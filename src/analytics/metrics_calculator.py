"""
Metrics calculation for kinematic properties.

Computes speed, acceleration, distance covered, and related metrics
from tracking data.
"""

import numpy as np
from typing import Dict, Tuple, Optional, List


class MetricsCalculator:
    """Calculates player and team metrics from tracking data."""

    # Speed thresholds (km/h)
    WALKING_THRESHOLD = 7
    JOGGING_THRESHOLD = 14
    RUNNING_THRESHOLD = 19
    SPRINTING_THRESHOLD = 24

    def __init__(self, fps: int = 10):
        """
        Initialize metrics calculator.

        Args:
            fps: Frames per second of tracking data
        """
        self.fps = fps
        self.frame_duration = 1.0 / fps

    def calculate_speed(
        self,
        position_history: np.ndarray
    ) -> np.ndarray:
        """
        Calculate instantaneous speed from position history.

        Args:
            position_history: Array of (n, 2) positions

        Returns:
            Array of speeds in m/s
        """
        if len(position_history) < 2:
            return np.zeros(len(position_history))

        # Calculate displacement
        displacements = np.diff(position_history, axis=0)
        distances = np.linalg.norm(displacements, axis=1)

        # Convert to speed (distance / time)
        speeds = distances / self.frame_duration

        # Prepend first speed for alignment
        speeds = np.insert(speeds, 0, speeds[0])
        return speeds

    def calculate_acceleration(
        self,
        speed_history: np.ndarray
    ) -> np.ndarray:
        """
        Calculate acceleration from speed history.

        Args:
            speed_history: Array of speeds

        Returns:
            Array of accelerations in m/s²
        """
        if len(speed_history) < 2:
            return np.zeros(len(speed_history))

        accelerations = np.diff(speed_history) / self.frame_duration
        accelerations = np.insert(accelerations, 0, accelerations[0])
        return accelerations

    def calculate_distance_covered(
        self,
        position_history: np.ndarray,
        frame_range: Optional[Tuple[int, int]] = None
    ) -> float:
        """
        Calculate total distance covered.

        Args:
            position_history: Array of positions
            frame_range: Optional (start, end) frame indices

        Returns:
            Distance in meters
        """
        if len(position_history) < 2:
            return 0.0

        if frame_range:
            start, end = frame_range
            position_history = position_history[start:end + 1]

        displacements = np.diff(position_history, axis=0)
        distances = np.linalg.norm(displacements, axis=1)
        return float(np.sum(distances))

    def calculate_distance_by_intensity(
        self,
        position_history: np.ndarray,
        speeds: np.ndarray
    ) -> Dict[str, float]:
        """
        Breakdown distance by intensity zones.

        Args:
            position_history: Array of positions
            speeds: Array of speeds

        Returns:
            Dict with distances for each intensity zone
        """
        if len(position_history) < 2:
            return {
                'walking': 0.0,
                'jogging': 0.0,
                'running': 0.0,
                'sprinting': 0.0
            }

        displacements = np.diff(position_history, axis=0)
        distances = np.linalg.norm(displacements, axis=1)

        result = {
            'walking': 0.0,
            'jogging': 0.0,
            'running': 0.0,
            'sprinting': 0.0
        }

        for i, dist in enumerate(distances):
            speed = speeds[i]
            if speed < self.WALKING_THRESHOLD:
                result['walking'] += dist
            elif speed < self.JOGGING_THRESHOLD:
                result['jogging'] += dist
            elif speed < self.RUNNING_THRESHOLD:
                result['running'] += dist
            else:
                result['sprinting'] += dist

        return result

    def detect_sprints(
        self,
        speeds: np.ndarray,
        min_duration_frames: int = 10
    ) -> List[Tuple[int, int]]:
        """
        Detect sprints (sustained high-speed effort).

        Args:
            speeds: Array of speeds
            min_duration_frames: Minimum sprint duration in frames

        Returns:
            List of (start_frame, end_frame) tuples
        """
        sprints = []
        in_sprint = False
        sprint_start = 0

        for i, speed in enumerate(speeds):
            if speed >= self.SPRINTING_THRESHOLD:
                if not in_sprint:
                    sprint_start = i
                    in_sprint = True
            else:
                if in_sprint:
                    duration = i - sprint_start
                    if duration >= min_duration_frames:
                        sprints.append((sprint_start, i - 1))
                    in_sprint = False

        # Handle sprint at end of history
        if in_sprint:
            duration = len(speeds) - sprint_start
            if duration >= min_duration_frames:
                sprints.append((sprint_start, len(speeds) - 1))

        return sprints

    def calculate_velocity_vector(
        self,
        position_history: np.ndarray
    ) -> Tuple[float, float]:
        """
        Calculate current velocity vector.

        Args:
            position_history: Recent position history

        Returns:
            Velocity (vx, vy) in m/s
        """
        if len(position_history) < 2:
            return (0.0, 0.0)

        displacement = position_history[-1] - position_history[0]
        time_elapsed = (len(position_history) - 1) * self.frame_duration

        vx = displacement[0] / time_elapsed
        vy = displacement[1] / time_elapsed

        return (float(vx), float(vy))
