"""
Heatmap generation from tracking data.

Aggregates player presence over time windows and generates spatial heatmaps.
"""

import numpy as np
from typing import Tuple, Optional


class HeatmapGenerator:
    """Generates heatmaps from tracking data."""

    def __init__(
        self,
        pitch_width: float = 105,
        pitch_height: float = 68,
        grid_size: Tuple[int, int] = (20, 15)
    ):
        """
        Initialize heatmap generator.

        Args:
            pitch_width: Pitch width in meters
            pitch_height: Pitch height in meters
            grid_size: Grid dimensions (width, height)
        """
        self.pitch_width = pitch_width
        self.pitch_height = pitch_height
        self.grid_width, self.grid_height = grid_size
        self.cell_width = pitch_width / self.grid_width
        self.cell_height = pitch_height / self.grid_height

    def generate_heatmap(
        self,
        positions: np.ndarray,
        frame_range: Optional[Tuple[int, int]] = None
    ) -> np.ndarray:
        """
        Generate presence heatmap.

        Args:
            positions: Array of (n_frames, 2) positions
            frame_range: Optional (start, end) frame indices

        Returns:
            2D heatmap array
        """
        heatmap = np.zeros((self.grid_height, self.grid_width))

        if frame_range:
            start, end = frame_range
            positions = positions[start:end + 1]

        # Accumulate cell counts
        for pos in positions:
            if len(pos) >= 2:
                x, y = pos[0], pos[1]

                # Check bounds
                if 0 <= x < self.pitch_width and 0 <= y < self.pitch_height:
                    cell_x = int(x / self.cell_width)
                    cell_y = int(y / self.cell_height)

                    # Clip to grid
                    cell_x = min(cell_x, self.grid_width - 1)
                    cell_y = min(cell_y, self.grid_height - 1)

                    heatmap[cell_y, cell_x] += 1

        # Normalize
        if heatmap.max() > 0:
            heatmap = heatmap / heatmap.max()

        return heatmap

    def generate_multi_player_heatmap(
        self,
        positions_list: list,
        frame_range: Optional[Tuple[int, int]] = None
    ) -> np.ndarray:
        """
        Generate combined heatmap for multiple players.

        Args:
            positions_list: List of position arrays
            frame_range: Optional frame range

        Returns:
            Combined heatmap
        """
        combined_heatmap = np.zeros((self.grid_height, self.grid_width))

        for positions in positions_list:
            heatmap = self.generate_heatmap(positions, frame_range)
            combined_heatmap += heatmap

        # Normalize
        if combined_heatmap.max() > 0:
            combined_heatmap = combined_heatmap / combined_heatmap.max()

        return combined_heatmap

    def generate_speed_heatmap(
        self,
        speeds: np.ndarray,
        positions: np.ndarray,
        frame_range: Optional[Tuple[int, int]] = None
    ) -> np.ndarray:
        """
        Generate heatmap weighted by movement speed.

        Args:
            speeds: Array of speeds
            positions: Array of positions
            frame_range: Optional frame range

        Returns:
            Speed-weighted heatmap
        """
        heatmap = np.zeros((self.grid_height, self.grid_width))

        if frame_range:
            start, end = frame_range
            speeds = speeds[start:end + 1]
            positions = positions[start:end + 1]

        # Accumulate weighted by speed
        for i, pos in enumerate(positions):
            if len(pos) >= 2:
                x, y = pos[0], pos[1]

                if 0 <= x < self.pitch_width and 0 <= y < self.pitch_height:
                    cell_x = int(x / self.cell_width)
                    cell_y = int(y / self.cell_height)

                    cell_x = min(cell_x, self.grid_width - 1)
                    cell_y = min(cell_y, self.grid_height - 1)

                    # Weight by speed
                    speed = speeds[i] if i < len(speeds) else 0
                    heatmap[cell_y, cell_x] += speed

        # Normalize
        if heatmap.max() > 0:
            heatmap = heatmap / heatmap.max()

        return heatmap
