"""
Spatial analysis for geometric relationships.

Computes pitch control, Voronoi diagrams, convex hulls, and
proximity-based metrics.
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
from scipy.spatial import ConvexHull, Voronoi


class SpatialAnalyzer:
    """Analyzes spatial relationships and team formations."""

    def __init__(self, pitch_width: float = 105, pitch_height: float = 68):
        """
        Initialize spatial analyzer.

        Args:
            pitch_width: Width of pitch in meters
            pitch_height: Height of pitch in meters
        """
        self.pitch_width = pitch_width
        self.pitch_height = pitch_height

    def compute_convex_hull(
        self,
        positions: np.ndarray
    ) -> Optional[ConvexHull]:
        """
        Compute convex hull of team positions.

        Args:
            positions: Array of (n, 2) positions

        Returns:
            ConvexHull object or None if insufficient points
        """
        if len(positions) < 3:
            return None

        try:
            return ConvexHull(positions)
        except Exception:
            return None

    def get_hull_area(self, hull: ConvexHull) -> float:
        """
        Get convex hull area.

        Args:
            hull: ConvexHull object

        Returns:
            Area in square meters
        """
        if hull is None:
            return 0.0
        return float(hull.volume)

    def compute_team_centroid(self, positions: np.ndarray) -> Tuple[float, float]:
        """
        Compute team center of mass.

        Args:
            positions: Array of (n, 2) positions

        Returns:
            Centroid (x, y)
        """
        if len(positions) == 0:
            return (0.0, 0.0)

        centroid = np.mean(positions, axis=0)
        return (float(centroid[0]), float(centroid[1]))

    def compute_team_compactness(self, positions: np.ndarray) -> float:
        """
        Compute team compactness (inverse of spread).

        Args:
            positions: Array of (n, 2) positions

        Returns:
            Compactness metric (0-1)
        """
        if len(positions) < 2:
            return 0.0

        centroid = np.mean(positions, axis=0)
        distances = np.linalg.norm(positions - centroid, axis=1)
        mean_distance = np.mean(distances)

        # Normalize to pitch dimensions
        max_possible = np.sqrt(self.pitch_width**2 + self.pitch_height**2)
        compactness = 1.0 - (mean_distance / max_possible)

        return float(np.clip(compactness, 0, 1))

    def get_nearest_opponent(
        self,
        player_pos: np.ndarray,
        opponent_positions: np.ndarray
    ) -> Tuple[float, int]:
        """
        Find nearest opponent to a player.

        Args:
            player_pos: (x, y) player position
            opponent_positions: Array of opponent positions

        Returns:
            (distance, opponent_index)
        """
        if len(opponent_positions) == 0:
            return (float('inf'), -1)

        distances = np.linalg.norm(opponent_positions - player_pos, axis=1)
        nearest_idx = np.argmin(distances)

        return (float(distances[nearest_idx]), int(nearest_idx))

    def get_nearest_teammate(
        self,
        player_pos: np.ndarray,
        teammate_positions: np.ndarray
    ) -> Tuple[float, int]:
        """
        Find nearest teammate to a player.

        Args:
            player_pos: (x, y) player position
            teammate_positions: Array of teammate positions

        Returns:
            (distance, teammate_index)
        """
        if len(teammate_positions) == 0:
            return (float('inf'), -1)

        distances = np.linalg.norm(teammate_positions - player_pos, axis=1)
        nearest_idx = np.argmin(distances)

        return (float(distances[nearest_idx]), int(nearest_idx))

    def compute_pitch_control(
        self,
        team1_positions: np.ndarray,
        team2_positions: np.ndarray,
        grid_size: Tuple[int, int] = (20, 15)
    ) -> np.ndarray:
        """
        Compute pitch control probability map using Voronoi.

        Args:
            team1_positions: Team 1 positions
            team2_positions: Team 2 positions
            grid_size: Grid dimensions (width, height)

        Returns:
            Probability map (0-1, team1 advantage)
        """
        control_map = np.zeros(grid_size)

        # Create grid points
        x = np.linspace(0, self.pitch_width, grid_size[0])
        y = np.linspace(0, self.pitch_height, grid_size[1])
        xx, yy = np.meshgrid(x, y)
        grid_points = np.column_stack((xx.ravel(), yy.ravel()))

        # Compute distances to each team
        for point_idx, point in enumerate(grid_points):
            dist_team1 = np.min(np.linalg.norm(team1_positions - point, axis=1))
            dist_team2 = np.min(np.linalg.norm(team2_positions - point, axis=1))

            # Control probability based on distance difference
            if dist_team1 < dist_team2:
                control_map.ravel()[point_idx] = dist_team2 / (dist_team1 + dist_team2)
            else:
                control_map.ravel()[point_idx] = 1.0 - (dist_team1 / (dist_team1 + dist_team2))

        return control_map.T
