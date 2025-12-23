"""
Test metrics calculations.
"""

import sys
from pathlib import Path
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analytics.metrics_calculator import MetricsCalculator


def test_speed_calculation():
    """Test speed calculation."""
    calc = MetricsCalculator(fps=10)

    # Create position history: moving 10 meters per frame
    positions = np.array([
        [0, 0],
        [10, 0],
        [20, 0]
    ])

    speeds = calc.calculate_speed(positions)
    # Each frame: 10m displacement, 0.1s duration = 100 m/s
    assert len(speeds) == len(positions)
    assert speeds[0] > 0
    print("✓ speed_calculation tests passed")


def test_distance_covered():
    """Test distance calculation."""
    calc = MetricsCalculator(fps=10)

    positions = np.array([
        [0, 0],
        [10, 0],
        [20, 0],
        [30, 0]
    ])

    distance = calc.calculate_distance_covered(positions)
    assert abs(distance - 30) < 0.1  # 30 meters
    print("✓ distance_covered tests passed")


def test_sprint_detection():
    """Test sprint detection."""
    calc = MetricsCalculator(fps=10)

    # Create speeds: 0-15 (walking), 25-30 (sprinting), 5 (walking)
    speeds = np.array(
        [5, 10, 15] +  # Walking/jogging
        [25, 26, 27, 28, 29, 30, 29, 28, 27] +  # Sprint (9 frames)
        [15, 10, 5]  # Walking
    )

    sprints = calc.detect_sprints(speeds, min_duration_frames=5)
    assert len(sprints) > 0
    start, end = sprints[0]
    assert end - start >= 5
    print("✓ sprint_detection tests passed")


def test_distance_by_intensity():
    """Test intensity zone breakdown."""
    calc = MetricsCalculator(fps=10)

    positions = np.array([
        [0, 0],
        [1, 0],  # Walking speed
        [10, 0],  # Running speed
        [25, 0]  # Sprint speed
    ])

    speeds = np.array([1, 5, 20, 30])

    breakdown = calc.calculate_distance_by_intensity(positions, speeds)
    assert 'walking' in breakdown
    assert 'jogging' in breakdown
    assert 'running' in breakdown
    assert 'sprinting' in breakdown
    print("✓ distance_by_intensity tests passed")


if __name__ == "__main__":
    print("Testing metrics calculations...\n")
    test_speed_calculation()
    test_distance_covered()
    test_sprint_detection()
    test_distance_by_intensity()
    print("\n✓ All metrics tests passed!")
