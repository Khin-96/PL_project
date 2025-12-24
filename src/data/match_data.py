"""
Match data parser for SkillCorner tracking data.
Handles loading, parsing, and caching of JSONL tracking files.
"""

import json
import jsonlines
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np
from dataclasses import dataclass

from utils.config import RAW_DATA_DIR, PROCESSED_DATA_DIR, DATA_FPS


@dataclass
class PlayerFrame:
    """Single frame of player tracking data."""
    player_id: int
    team_id: int
    jersey_number: int
    x: float
    y: float
    timestamp: float


@dataclass
class BallFrame:
    """Single frame of ball tracking data."""
    x: float
    y: float
    z: float
    timestamp: float


@dataclass
class MatchFrame:
    """Complete frame of match data."""
    frame_id: int
    timestamp: float
    players: List[PlayerFrame]
    ball: Optional[BallFrame]


class MatchDataLoader:
    """Loads and manages match tracking data from SkillCorner format."""
    
    def __init__(self, match_id: str):
        """
        Initialize loader for a specific match.
        
        Args:
            match_id: SkillCorner match identifier
        """
        self.match_id = match_id
        self.raw_dir = Path(RAW_DATA_DIR)
        self.processed_dir = Path(PROCESSED_DATA_DIR)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        self.metadata = None
        self.frames = []
        self.player_info = {}
        
    def load_metadata(self) -> Dict:
        """
        Load match metadata from JSON file.
        
        Returns:
            Dictionary containing match metadata
        """
        metadata_path = self.raw_dir / f"{self.match_id}_match.json"
        
        if not metadata_path.exists():
            raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
        
        with open(metadata_path, 'r') as f:
            self.metadata = json.load(f)
        
        # Parse player information
        for team in ['home_team', 'away_team']:
            team_data = self.metadata.get(team, {})
            team_id = team_data.get('id', 0)
            
            for player in team_data.get('players', []):
                player_id = player.get('id')
                self.player_info[player_id] = {
                    'name': player.get('name', 'Unknown'),
                    'jersey_number': player.get('jersey_number', 0),
                    'team_id': team_id,
                    'team_name': team_data.get('name', 'Unknown'),
                    'position': player.get('position', 'Unknown')
                }
        
        return self.metadata
    
    def load_tracking_data(self) -> List[MatchFrame]:
        """
        Load tracking data from JSONL file.
        
        Returns:
            List of MatchFrame objects
        """
        tracking_path = self.raw_dir / f"{self.match_id}_tracking_extrapolated.jsonl"
        
        if not tracking_path.exists():
            raise FileNotFoundError(f"Tracking file not found: {tracking_path}")
        
        print(f"Loading tracking data from {tracking_path}...")
        
        frames = []
        with jsonlines.open(tracking_path) as reader:
            for idx, line in enumerate(reader):
                frame = self._parse_frame(idx, line)
                if frame:
                    frames.append(frame)
                
                if idx % 1000 == 0 and idx > 0:
                    print(f"  Loaded {idx} frames...")
        
        self.frames = frames
        print(f"Loaded {len(frames)} frames total")
        return frames
    
    def _parse_frame(self, frame_id: int, data: Dict) -> Optional[MatchFrame]:
        """
        Parse a single frame from JSONL data.
        
        Args:
            frame_id: Sequential frame identifier
            data: Raw frame data dictionary
            
        Returns:
            MatchFrame object or None if invalid
        """
        try:
            # Parse timestamp - handle None, string timestamps, or numeric values
            raw_timestamp = data.get('timestamp')
            if raw_timestamp is None:
                timestamp = frame_id / DATA_FPS
            elif isinstance(raw_timestamp, str):
                # Handle string timestamps like '00:00:00.00'
                # Convert HH:MM:SS.MS to seconds
                parts = raw_timestamp.split(':')
                if len(parts) == 3:
                    hours = float(parts[0])
                    minutes = float(parts[1])
                    seconds = float(parts[2])
                    timestamp = hours * 3600 + minutes * 60 + seconds
                else:
                    timestamp = frame_id / DATA_FPS
            else:
                timestamp = float(raw_timestamp)
            
            # Parse player positions
            players = []
            for player_data in data.get('player_data', []):
                if isinstance(player_data, dict):
                    player = PlayerFrame(
                        player_id=player_data.get('player_id'),
                        team_id=player_data.get('team_id', 0),
                        jersey_number=player_data.get('jersey_number', 0),
                        x=player_data.get('x', 0.0),
                        y=player_data.get('y', 0.0),
                        timestamp=timestamp
                    )
                    players.append(player)
            
            # Parse ball position
            ball = None
            ball_data = data.get('ball_data', {})
            if isinstance(ball_data, dict) and ('x' in ball_data or 'y' in ball_data):
                ball = BallFrame(
                    x=ball_data.get('x', 0.0),
                    y=ball_data.get('y', 0.0),
                    z=ball_data.get('z', 0.0),
                    timestamp=timestamp
                )
            
            return MatchFrame(
                frame_id=frame_id,
                timestamp=timestamp,
                players=players,
                ball=ball
            )
            
        except Exception as e:
            print(f"Error parsing frame {frame_id}: {e}")
            return None
    
    def save_to_cache(self):
        """
        Save processed data to numpy cache for faster loading.
        """
        cache_path = self.processed_dir / f"{self.match_id}_cache.npz"
        
        print(f"Saving cache to {cache_path}...")
        
        # Convert frames to numpy arrays
        num_frames = len(self.frames)
        max_players = max(len(f.players) for f in self.frames)
        
        # Player data: [frame, player, [x, y, player_id, team_id, jersey]]
        player_data = np.zeros((num_frames, max_players, 5), dtype=np.float32)
        player_data.fill(np.nan)
        
        # Ball data: [frame, [x, y, z]]
        ball_data = np.zeros((num_frames, 3), dtype=np.float32)
        ball_data.fill(np.nan)
        
        # Timestamps
        timestamps = np.zeros(num_frames, dtype=np.float32)
        
        for i, frame in enumerate(self.frames):
            timestamps[i] = frame.timestamp
            
            for j, player in enumerate(frame.players):
                player_data[i, j] = [
                    player.x,
                    player.y,
                    player.player_id,
                    player.team_id,
                    player.jersey_number
                ]
            
            if frame.ball:
                ball_data[i] = [frame.ball.x, frame.ball.y, frame.ball.z]
        
        np.savez_compressed(
            cache_path,
            player_data=player_data,
            ball_data=ball_data,
            timestamps=timestamps,
            metadata=json.dumps(self.metadata),
            player_info=json.dumps(self.player_info)
        )
        
        print("Cache saved successfully")
    
    def load_from_cache(self) -> bool:
        """
        Load data from numpy cache if available.
        
        Returns:
            True if cache was loaded successfully
        """
        cache_path = self.processed_dir / f"{self.match_id}_cache.npz"
        
        if not cache_path.exists():
            return False
        
        print(f"Loading from cache: {cache_path}")
        
        try:
            data = np.load(cache_path, allow_pickle=True)
            
            player_data = data['player_data']
            ball_data = data['ball_data']
            timestamps = data['timestamps']
            self.metadata = json.loads(str(data['metadata']))
            self.player_info = json.loads(str(data['player_info']))
            
            # Reconstruct frames
            self.frames = []
            for i in range(len(timestamps)):
                players = []
                for j in range(player_data.shape[1]):
                    if not np.isnan(player_data[i, j, 0]):
                        players.append(PlayerFrame(
                            player_id=int(player_data[i, j, 2]),
                            team_id=int(player_data[i, j, 3]),
                            jersey_number=int(player_data[i, j, 4]),
                            x=float(player_data[i, j, 0]),
                            y=float(player_data[i, j, 1]),
                            timestamp=float(timestamps[i])
                        ))
                
                ball = None
                if not np.isnan(ball_data[i, 0]):
                    ball = BallFrame(
                        x=float(ball_data[i, 0]),
                        y=float(ball_data[i, 1]),
                        z=float(ball_data[i, 2]),
                        timestamp=float(timestamps[i])
                    )
                
                self.frames.append(MatchFrame(
                    frame_id=i,
                    timestamp=float(timestamps[i]),
                    players=players,
                    ball=ball
                ))
            
            print(f"Loaded {len(self.frames)} frames from cache")
            return True
            
        except Exception as e:
            print(f"Error loading cache: {e}")
            return False
    
    def get_frame(self, frame_id: int) -> Optional[MatchFrame]:
        """
        Get a specific frame by ID.
        
        Args:
            frame_id: Frame identifier
            
        Returns:
            MatchFrame or None if out of bounds
        """
        if 0 <= frame_id < len(self.frames):
            return self.frames[frame_id]
        return None
    
    def get_frame_at_timestamp(self, timestamp: float) -> Optional[MatchFrame]:
        """
        Get the frame closest to a specific timestamp.
        
        Args:
            timestamp: Time in seconds
            
        Returns:
            MatchFrame or None
        """
        if not self.frames:
            return None
        
        # Binary search for closest frame
        closest_idx = min(
            range(len(self.frames)),
            key=lambda i: abs(self.frames[i].timestamp - timestamp)
        )
        return self.frames[closest_idx]
    
    def get_player_name(self, player_id: int) -> str:
        """Get player name from ID."""
        return self.player_info.get(player_id, {}).get('name', f'Player {player_id}')
    
    def get_total_frames(self) -> int:
        """Get total number of frames."""
        return len(self.frames)
    
    def get_duration(self) -> float:
        """Get match duration in seconds."""
        if not self.frames:
            return 0.0
        return self.frames[-1].timestamp