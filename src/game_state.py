"""
Central game state manager that coordinates all components of the replay system.
"""

from typing import Optional, List, Dict
from dataclasses import dataclass

from data.match_data import MatchDataLoader, MatchFrame
from utils.config import PLAYBACK_SPEEDS, DEFAULT_PLAYBACK_SPEED, DATA_FPS


@dataclass
class OverlayState:
    """Tracks which overlays are currently active."""
    heatmap: bool = False
    pass_network: bool = False
    formation: bool = False
    pressure_map: bool = False


class GameState:
    """
    Manages the complete state of the match replay.
    Acts as the central coordinator between data, rendering, and user input.
    """
    
    def __init__(self, match_id: str):
        """
        Initialize game state for a specific match.
        
        Args:
            match_id: SkillCorner match identifier
        """
        self.match_id = match_id
        
        # Load match data
        self.data_loader = MatchDataLoader(match_id)
        print("Loading match data...")
        
        # Try cache first, fall back to raw files
        if not self.data_loader.load_from_cache():
            self.data_loader.load_metadata()
            self.data_loader.load_tracking_data()
            self.data_loader.save_to_cache()
        
        # Playback state
        self.current_frame_index = 0
        self.is_paused = False
        self.playback_speed = DEFAULT_PLAYBACK_SPEED
        self.playback_speed_index = PLAYBACK_SPEEDS.index(DEFAULT_PLAYBACK_SPEED)
        
        # Frame timing
        self.frame_accumulator = 0.0
        self.frames_per_second = DATA_FPS
        
        # Selection state
        self.selected_player_id: Optional[int] = None
        
        # Overlay toggles
        self.overlays = OverlayState()
        
        # UI state
        self.show_timeline = True
        self.show_telemetry = True
        
        # Cache current frame for quick access
        self._current_frame: Optional[MatchFrame] = None
        self._update_current_frame()
    
    def update(self, delta_time: float):
        """
        Update game state based on elapsed time.
        Called every frame from the main game loop.
        
        Args:
            delta_time: Time elapsed since last update in seconds
        """
        if self.is_paused:
            return
        
        # Accumulate time based on playback speed
        self.frame_accumulator += delta_time * self.playback_speed
        
        # Advance frames when we've accumulated enough time
        frames_to_advance = int(self.frame_accumulator * self.frames_per_second)
        if frames_to_advance > 0:
            self.frame_accumulator -= frames_to_advance / self.frames_per_second
            self.advance_frames(frames_to_advance)
    
    def advance_frames(self, num_frames: int):
        """
        Move forward by a number of frames.
        
        Args:
            num_frames: Number of frames to advance
        """
        self.current_frame_index = min(
            self.current_frame_index + num_frames,
            self.get_total_frames() - 1
        )
        self._update_current_frame()
    
    def rewind_frames(self, num_frames: int):
        """
        Move backward by a number of frames.
        
        Args:
            num_frames: Number of frames to rewind
        """
        self.current_frame_index = max(0, self.current_frame_index - num_frames)
        self._update_current_frame()
    
    def seek_to_frame(self, frame_index: int):
        """
        Jump to a specific frame.
        
        Args:
            frame_index: Target frame index
        """
        self.current_frame_index = max(0, min(frame_index, self.get_total_frames() - 1))
        self._update_current_frame()
    
    def seek_to_timestamp(self, timestamp: float):
        """
        Jump to a specific time in the match.
        
        Args:
            timestamp: Target timestamp in seconds
        """
        # Calculate frame index from timestamp
        frame_index = int(timestamp * self.frames_per_second)
        self.seek_to_frame(frame_index)
    
    def _update_current_frame(self):
        """Update the cached current frame."""
        self._current_frame = self.data_loader.get_frame(self.current_frame_index)
    
    def get_current_frame(self) -> Optional[MatchFrame]:
        """Get the current frame data."""
        return self._current_frame
    
    def toggle_pause(self):
        """Toggle between paused and playing."""
        self.is_paused = not self.is_paused
    
    def set_playback_speed(self, speed: float):
        """
        Set playback speed.
        
        Args:
            speed: Speed multiplier (0.25, 0.5, 1.0, 2.0, 4.0)
        """
        if speed in PLAYBACK_SPEEDS:
            self.playback_speed = speed
            self.playback_speed_index = PLAYBACK_SPEEDS.index(speed)
    
    def cycle_playback_speed(self):
        """Cycle through available playback speeds."""
        self.playback_speed_index = (self.playback_speed_index + 1) % len(PLAYBACK_SPEEDS)
        self.playback_speed = PLAYBACK_SPEEDS[self.playback_speed_index]
    
    def restart(self):
        """Reset to the beginning of the match."""
        self.current_frame_index = 0
        self.frame_accumulator = 0.0
        self._update_current_frame()
    
    def select_player(self, player_id: int):
        """
        Select a player for detailed tracking.
        
        Args:
            player_id: ID of player to select
        """
        self.selected_player_id = player_id
    
    def deselect_player(self):
        """Clear player selection."""
        self.selected_player_id = None
    
    def is_player_selected(self, player_id: int) -> bool:
        """Check if a specific player is selected."""
        return self.selected_player_id == player_id
    
    def get_selected_player_name(self) -> str:
        """Get name of currently selected player."""
        if self.selected_player_id is None:
            return "No player selected"
        return self.data_loader.get_player_name(self.selected_player_id)
    
    def toggle_overlay(self, overlay_name: str):
        """
        Toggle a specific overlay on/off.
        
        Args:
            overlay_name: Name of overlay (heatmap, pass_network, formation, pressure_map)
        """
        if hasattr(self.overlays, overlay_name):
            current = getattr(self.overlays, overlay_name)
            setattr(self.overlays, overlay_name, not current)
    
    def get_current_timestamp(self) -> float:
        """Get current timestamp in seconds."""
        if self._current_frame:
            return self._current_frame.timestamp
        return 0.0
    
    def get_total_frames(self) -> int:
        """Get total number of frames in match."""
        return self.data_loader.get_total_frames()
    
    def get_total_duration(self) -> float:
        """Get total match duration in seconds."""
        return self.data_loader.get_duration()
    
    def get_progress_percentage(self) -> float:
        """Get current progress through match as percentage."""
        total = self.get_total_frames()
        if total == 0:
            return 0.0
        return (self.current_frame_index / total) * 100.0
    
    def format_time(self, seconds: float) -> str:
        """
        Format seconds as MM:SS.
        
        Args:
            seconds: Time in seconds
            
        Returns:
            Formatted string like "12:34"
        """
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
    
    def get_metadata(self) -> Dict:
        """Get match metadata."""
        return self.data_loader.metadata or {}
    
    def get_player_info(self, player_id: int) -> Dict:
        """
        Get information about a specific player.
        
        Args:
            player_id: Player identifier
            
        Returns:
            Dictionary with player information
        """
        return self.data_loader.player_info.get(player_id, {})