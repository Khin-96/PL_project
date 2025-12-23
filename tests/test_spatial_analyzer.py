"""
Test spatial analysis algorithms.
"""

import sys
from pathlib import Path
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analytics.spatial_analyzer import SpatialAnalyzer


def test_centroid():
    """Test centroid calculation."""
    analyzer = SpatialAnalyzer()

    positions = np.array([
        [0, 0],
        [10, 0],
        [10, 10],
        [0, 10]
    ])

    centroid = analyzer.compute_team_centroid(positions)
    assert abs(centroid[0] - 5) < 0.01
    assert abs(centroid[1] - 5) < 0.01
    print("✓ centroid tests passed")


def test_compactness():
    """Test team compactness calculation."""
    analyzer = SpatialAnalyzer()

    # Tightly grouped
    tight_positions = np.array([
        [50, 34],
        [50, 35],
        [50, 33],
        [51, 34]
    ])

    compactness_tight = analyzer.compute_team_compactness(tight_positions)
    assert compactness_tight > 0.5
    print("✓ compactness: tight")

    # Spread out
    spread_positions = np.array([
        [10, 10],
        [50, 34],
        [95, 60],
        [30, 20]
    ])

    compactness_spread = analyzer.compute_team_compactness(spread_positions)
    assert compactness_spread < compactness_tight
    print("✓ compactness: spread")

    print("✓ compactness tests passed")


def test_nearest_opponent():
    """Test nearest opponent detection."""
    analyzer = SpatialAnalyzer()

    player_pos = np.array([50, 34])
    opponent_positions = np.array([
        [52, 34],
        [60, 40],
        [40, 30]
    ])

    distance, idx = analyzer.get_nearest_opponent(player_pos, opponent_positions)
    assert idx == 0  # Nearest is first opponent
    assert distance < 5
    print("✓ nearest_opponent tests passed")


def test_pitch_control():
    """Test pitch control calculation."""
    analyzer = SpatialAnalyzer()

    team1_positions = np.array([
        [30, 34],
        [40, 40],
        [40, 28]
    ])

    team2_positions = np.array([
        [70, 34],
        [80, 40],
        [80, 28]
    ])

    control = analyzer.compute_pitch_control(team1_positions, team2_positions)
    assert control.shape == (15, 20)  # Default grid
    assert np.all((control >= 0) & (control <= 1))
    print("✓ pitch_control tests passed")


if __name__ == "__main__":
    print("Testing spatial analysis...\n")
    test_centroid()
    test_compactness()
    test_nearest_opponent()
    test_pitch_control()
    print("\n✓ All spatial analysis tests passed!")
