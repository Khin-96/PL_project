"""
Sprite animation and smooth interpolation.

Handles smooth movement between tracking data frames using
cubic spline and linear interpolation.
"""

from typing import Tuple, List
import numpy as np
from scipy.interpolate import CubicSpline


class SpriteAnimator:
    """Manages smooth sprite animation between frames."""

    def __init__(self, fps_source: int = 10, fps_display: int = 60):
        """
        Initialize animator.

        Args:
            fps_source: Source tracking data FPS
            fps_display: Display/rendering FPS
        """
        self.fps_source = fps_source
        self.fps_display = fps_display
        self.interpolation_factor = fps_display / fps_source
        self._spline_cache = {}

    def interpolate_position(
        self,
        positions: List[Tuple[float, float]],
        frame_indices: List[int],
        target_frame: float
    ) -> Tuple[float, float]:
        """
        Interpolate position at a target frame using cubic splines.

        Args:
            positions: List of (x, y) positions
            frame_indices: Corresponding frame numbers
            target_frame: Frame to interpolate to

        Returns:
            Interpolated (x, y) position
        """
        if len(positions) < 2:
            return positions[0] if positions else (0, 0)

        frame_indices = np.array(frame_indices, dtype=float)
        positions = np.array(positions)

        # Create cubic spline for x and y coordinates
        try:
            spline_x = CubicSpline(frame_indices, positions[:, 0])
            spline_y = CubicSpline(frame_indices, positions[:, 1])

            x = float(spline_x(target_frame))
            y = float(spline_y(target_frame))
            return (x, y)
        except Exception:
            # Fall back to linear interpolation if spline fails
            return self.interpolate_linear(positions, frame_indices, target_frame)

    def interpolate_linear(
        self,
        positions: List[Tuple[float, float]],
        frame_indices: List[int],
        target_frame: float
    ) -> Tuple[float, float]:
        """
        Linear interpolation between positions.

        Args:
            positions: List of (x, y) positions
            frame_indices: Corresponding frame numbers
            target_frame: Frame to interpolate to

        Returns:
            Interpolated (x, y) position
        """
        frame_indices = np.array(frame_indices, dtype=float)
        positions = np.array(positions)

        # Find surrounding frames
        if target_frame <= frame_indices[0]:
            return tuple(positions[0])
        if target_frame >= frame_indices[-1]:
            return tuple(positions[-1])

        idx = np.searchsorted(frame_indices, target_frame)
        f1, f2 = frame_indices[idx - 1], frame_indices[idx]
        p1, p2 = positions[idx - 1], positions[idx]

        # Linear interpolation
        t = (target_frame - f1) / (f2 - f1)
        x = p1[0] + t * (p2[0] - p1[0])
        y = p1[1] + t * (p2[1] - p1[1])

        return (x, y)

    def get_velocity(
        self,
        positions: List[Tuple[float, float]],
        time_steps: float = 0.1
    ) -> Tuple[float, float]:
        """
        Calculate velocity from position history.

        Args:
            positions: Recent position history
            time_steps: Time window in seconds

        Returns:
            Velocity (vx, vy)
        """
        if len(positions) < 2:
            return (0, 0)

        p1 = np.array(positions[0])
        p2 = np.array(positions[-1])
        displacement = p2 - p1

        vx = displacement[0] / time_steps
        vy = displacement[1] / time_steps

        return (float(vx), float(vy))
