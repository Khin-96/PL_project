"""
Test interpolation methods.
"""

import sys
from pathlib import Path
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.interpolation import (
    linear_interpolate,
    cubic_interpolate,
    catmull_rom_interpolate
)


def test_linear_interpolate():
    """Test linear interpolation."""
    p1 = (0, 0)
    p2 = (10, 10)

    # Midpoint
    result = linear_interpolate(p1, p2, 0.5)
    assert abs(result[0] - 5) < 0.01
    assert abs(result[1] - 5) < 0.01
    print("✓ linear_interpolate: midpoint")

    # Start point
    result = linear_interpolate(p1, p2, 0.0)
    assert abs(result[0] - 0) < 0.01
    assert abs(result[1] - 0) < 0.01
    print("✓ linear_interpolate: start")

    # End point
    result = linear_interpolate(p1, p2, 1.0)
    assert abs(result[0] - 10) < 0.01
    assert abs(result[1] - 10) < 0.01
    print("✓ linear_interpolate: end")

    print("✓ linear_interpolate tests passed")


def test_cubic_interpolate():
    """Test cubic spline interpolation."""
    points = [(0, 0), (10, 10), (20, 5), (30, 15)]
    t_values = [0, 1, 2, 3]

    # Interpolate at t=1.5
    result = cubic_interpolate(points, t_values, 1.5)
    assert result is not None
    assert len(result) == 2
    print("✓ cubic_interpolate: interpolation")

    # At control point
    result = cubic_interpolate(points, t_values, 1.0)
    assert abs(result[0] - 10) < 0.1
    assert abs(result[1] - 10) < 0.1
    print("✓ cubic_interpolate: at control point")

    print("✓ cubic_interpolate tests passed")


def test_catmull_rom():
    """Test Catmull-Rom interpolation."""
    p0 = (0, 0)
    p1 = (10, 10)
    p2 = (20, 5)
    p3 = (30, 15)

    # Midpoint between p1 and p2
    result = catmull_rom_interpolate(p0, p1, p2, p3, 0.5)
    assert result is not None
    assert len(result) == 2
    print("✓ catmull_rom: interpolation")

    print("✓ catmull_rom tests passed")


if __name__ == "__main__":
    print("Testing interpolation methods...\n")
    test_linear_interpolate()
    test_cubic_interpolate()
    test_catmull_rom()
    print("\n✓ All interpolation tests passed!")
