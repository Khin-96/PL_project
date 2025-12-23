"""
Tactical analysis for formations and pressing.

Detects team formations, transitions, and defensive pressure patterns.
"""

import numpy as np
from typing import Dict, Tuple, Optional, List


class TacticalAnalyzer:
    """Analyzes tactical formations and patterns."""

    FORMATIONS = {
        '3-5-2': {'def': 3, 'mid': 5, 'att': 2},
        '4-3-3': {'def': 4, 'mid': 3, 'att': 3},
        '4-4-2': {'def': 4, 'mid': 4, 'att': 2},
        '5-3-2': {'def': 5, 'mid': 3, 'att': 2},
        '5-4-1': {'def': 5, 'mid': 4, 'att': 1},
        '4-2-4': {'def': 4, 'mid': 2, 'att': 4},
    }

    def __init__(self, pitch_width: float = 105, pitch_height: float = 68):
        """
        Initialize tactical analyzer.

        Args:
            pitch_width: Pitch width in meters
            pitch_height: Pitch height in meters
        """
        self.pitch_width = pitch_width
        self.pitch_height = pitch_height

    def detect_formation(
        self,
        positions: np.ndarray
    ) -> Tuple[str, Dict]:
        """
        Detect team formation.

        Args:
            positions: Array of (n, 2) player positions

        Returns:
            (formation_name, formation_dict)
        """
        if len(positions) < 10:
            return 'Unknown', {}

        # Sort players by x-coordinate (defensive to attacking)
        sorted_positions = positions[np.argsort(positions[:, 0])]

        # Divide into thirds
        third_width = self.pitch_width / 3

        defensive_third = sorted_positions[sorted_positions[:, 0] < third_width]
        middle_third = sorted_positions[
            (sorted_positions[:, 0] >= third_width) &
            (sorted_positions[:, 0] < 2 * third_width)
        ]
        attacking_third = sorted_positions[sorted_positions[:, 0] >= 2 * third_width]

        # Get counts
        def_count = len(defensive_third)
        mid_count = len(middle_third)
        att_count = len(attacking_third)

        # Find matching formation
        formation_key = f"{def_count}-{mid_count}-{att_count}"
        formation = self.FORMATIONS.get(formation_key, {})

        return formation_key, formation

    def calculate_defensive_line_height(
        self,
        team_positions: np.ndarray
    ) -> float:
        """
        Get defensive line y-coordinate.

        Args:
            team_positions: Array of team positions

        Returns:
            Y-coordinate of deepest defender
        """
        if len(team_positions) == 0:
            return self.pitch_height / 2

        # Find minimum x (most defensive)
        min_x = np.min(team_positions[:, 0])
        defensive_line_players = team_positions[team_positions[:, 0] == min_x]

        # Return average y-coordinate
        return float(np.mean(defensive_line_players[:, 1]))

    def calculate_team_shape(
        self,
        positions: np.ndarray
    ) -> Dict:
        """
        Calculate team shape metrics.

        Args:
            positions: Array of positions

        Returns:
            Dict with shape metrics
        """
        if len(positions) == 0:
            return {}

        shape = {
            'width': float(np.max(positions[:, 1]) - np.min(positions[:, 1])),
            'depth': float(np.max(positions[:, 0]) - np.min(positions[:, 0])),
            'centroid_x': float(np.mean(positions[:, 0])),
            'centroid_y': float(np.mean(positions[:, 1])),
        }

        return shape

    def calculate_pressing_intensity(
        self,
        defending_team: np.ndarray,
        attacking_team: np.ndarray,
        ball_pos: np.ndarray
    ) -> float:
        """
        Calculate defensive pressing intensity.

        Args:
            defending_team: Defending team positions
            attacking_team: Attacking team positions
            ball_pos: Ball position

        Returns:
            Pressing intensity (0-1)
        """
        if len(defending_team) == 0:
            return 0.0

        # Calculate average distance from defenders to attackers
        avg_distances = []
        for attacker in attacking_team:
            min_dist = np.min(np.linalg.norm(defending_team - attacker, axis=1))
            avg_distances.append(min_dist)

        avg_dist = np.mean(avg_distances)

        # Normalize to intensity (closer = more intense)
        max_distance = 30  # Maximum relevant distance
        intensity = 1.0 - (avg_dist / max_distance)

        return float(np.clip(intensity, 0, 1))

    def detect_offside_line(
        self,
        defending_team: np.ndarray,
        ball_x: float
    ) -> float:
        """
        Detect offside line position.

        Args:
            defending_team: Defending team positions
            ball_x: Ball x-coordinate

        Returns:
            Offside line x-coordinate
        """
        if len(defending_team) == 0:
            return ball_x

        # Deepest defender (minimum x)
        offside_line = np.min(defending_team[:, 0])

        # Ball position matters for offside
        if ball_x < offside_line:
            offside_line = ball_x

        return float(offside_line)
