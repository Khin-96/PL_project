"""
Data caching and binary format conversion.

Converts JSONL tracking data to efficient binary formats (NumPy .npz)
for faster loading and memory-mapped access.
"""

import numpy as np
from pathlib import Path
from typing import Optional, Tuple
import json


class DataCache:
    """Manages conversion and caching of tracking data."""

    def __init__(self, cache_dir: str = "data/processed"):
        """
        Initialize data cache manager.

        Args:
            cache_dir: Directory for cached data
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_cache_path(self, match_id: int) -> Path:
        """
        Get cache file path for a match.

        Args:
            match_id: Match ID

        Returns:
            Path to cache file
        """
        return self.cache_dir / f"{match_id}_tracking.npz"

    def is_cached(self, match_id: int) -> bool:
        """
        Check if match is cached.

        Args:
            match_id: Match ID

        Returns:
            True if cache exists
        """
        return self.get_cache_path(match_id).exists()

    def load_cache(
        self,
        match_id: int
    ) -> Optional[Tuple[np.ndarray, np.ndarray, np.ndarray]]:
        """
        Load cached tracking data.

        Args:
            match_id: Match ID

        Returns:
            Tuple of (frames, player_positions, ball_position) or None
        """
        cache_path = self.get_cache_path(match_id)
        if not cache_path.exists():
            return None

        try:
            data = np.load(cache_path, mmap_mode='r')
            return (
                data['frames'],
                data['player_positions'],
                data['ball_position']
            )
        except Exception as e:
            print(f"Error loading cache: {e}")
            return None

    def save_cache(
        self,
        match_id: int,
        frames: np.ndarray,
        player_positions: np.ndarray,
        ball_position: np.ndarray
    ) -> bool:
        """
        Save tracking data to cache.

        Args:
            match_id: Match ID
            frames: Frame indices
            player_positions: Player position data
            ball_position: Ball position data

        Returns:
            True if successful
        """
        try:
            cache_path = self.get_cache_path(match_id)
            np.savez_compressed(
                cache_path,
                frames=frames,
                player_positions=player_positions,
                ball_position=ball_position
            )
            return True
        except Exception as e:
            print(f"Error saving cache: {e}")
            return False

    def clear_cache(self, match_id: int) -> bool:
        """
        Delete cached data for a match.

        Args:
            match_id: Match ID

        Returns:
            True if successful
        """
        try:
            cache_path = self.get_cache_path(match_id)
            if cache_path.exists():
                cache_path.unlink()
            return True
        except Exception as e:
            print(f"Error clearing cache: {e}")
            return False
