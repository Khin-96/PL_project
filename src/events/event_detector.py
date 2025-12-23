"""
Event detection algorithms.

Detects significant events from tracking data when event data unavailable.
"""

import numpy as np
from typing import List, Dict, Tuple


class EventDetector:
    """Detects events from tracking data."""

    def __init__(self):
        """Initialize event detector."""
        pass

    def detect_goals(
        self,
        ball_positions: np.ndarray,
        goal_threshold: float = 2.0
    ) -> List[Dict]:
        """
        Detect goal events from ball movement.

        Args:
            ball_positions: Array of ball positions
            goal_threshold: Distance threshold for goal detection

        Returns:
            List of goal events
        """
        goals = []

        # Detect when ball crosses goal line
        for i in range(len(ball_positions) - 1):
            x1, y1 = ball_positions[i]
            x2, y2 = ball_positions[i + 1]

            # Check if ball crossed goal line (x=0 or x=105)
            if (x1 > 0 and x2 <= 0) or (x1 < 105 and x2 >= 105):
                goals.append({
                    'type': 'goal',
                    'frame': i,
                    'position': (x2, y2)
                })

        return goals

    def detect_shots(
        self,
        ball_positions: np.ndarray,
        ball_speeds: np.ndarray,
        speed_threshold: float = 20.0
    ) -> List[Dict]:
        """
        Detect shot events from ball speed.

        Args:
            ball_positions: Array of ball positions
            ball_speeds: Array of ball speeds
            speed_threshold: Speed threshold for shot detection

        Returns:
            List of shot events
        """
        shots = []

        for i in range(len(ball_speeds)):
            if ball_speeds[i] > speed_threshold:
                # Check if in attacking area
                x, y = ball_positions[i]
                if x > 70:  # Attacking third
                    shots.append({
                        'type': 'shot',
                        'frame': i,
                        'position': (x, y),
                        'speed': ball_speeds[i]
                    })

        return shots

    def detect_passes(
        self,
        ball_positions: np.ndarray,
        player_possession: np.ndarray
    ) -> List[Dict]:
        """
        Detect pass events from possession changes.

        Args:
            ball_positions: Array of ball positions
            player_possession: Array of player IDs with possession

        Returns:
            List of pass events
        """
        passes = []

        for i in range(1, len(player_possession)):
            if player_possession[i] != player_possession[i - 1]:
                # Possession changed (pass occurred)
                passes.append({
                    'type': 'pass',
                    'frame': i,
                    'passer': player_possession[i - 1],
                    'receiver': player_possession[i],
                    'position': tuple(ball_positions[i])
                })

        return passes

    def detect_fouls(
        self,
        player_distances: np.ndarray,
        distance_threshold: float = 1.0
    ) -> List[Dict]:
        """
        Detect potential foul events.

        Args:
            player_distances: Array of distances between players
            distance_threshold: Distance threshold for contact

        Returns:
            List of potential foul events
        """
        fouls = []

        for i in range(len(player_distances)):
            if player_distances[i] < distance_threshold:
                fouls.append({
                    'type': 'contact',
                    'frame': i,
                    'distance': player_distances[i]
                })

        return fouls
