"""
Interpolation utilities for smooth movement.

Provides cubic spline and linear interpolation for smooth motion.
"""

from typing import List, Tuple, Optional
import numpy as np
from scipy.interpolate import CubicSpline


def linear_interpolate(
    p1: Tuple[float, float],
    p2: Tuple[float, float],
    t: float
) -> Tuple[float, float]:
    """
    Linear interpolation between two points.

    Args:
        p1: Start point (x, y)
        p2: End point (x, y)
        t: Interpolation factor (0-1)

    Returns:
        Interpolated point
    """
    x = p1[0] + t * (p2[0] - p1[0])
    y = p1[1] + t * (p2[1] - p1[1])
    return (x, y)


def cubic_interpolate(
    points: List[Tuple[float, float]],
    t_values: List[float],
    t_target: float
) -> Optional[Tuple[float, float]]:
    """
    Cubic spline interpolation.

    Args:
        points: List of (x, y) points
        t_values: Parameter values for points
        t_target: Target parameter value

    Returns:
        Interpolated point or None
    """
    if len(points) < 2:
        return points[0] if points else None

    try:
        points = np.array(points)
        t_values = np.array(t_values)

        spline_x = CubicSpline(t_values, points[:, 0])
        spline_y = CubicSpline(t_values, points[:, 1])

        x = float(spline_x(t_target))
        y = float(spline_y(t_target))

        return (x, y)
    except Exception:
        # Fallback to linear
        return linear_interpolate(points[0], points[-1], 0.5)


def catmull_rom_interpolate(
    p0: Tuple[float, float],
    p1: Tuple[float, float],
    p2: Tuple[float, float],
    p3: Tuple[float, float],
    t: float
) -> Tuple[float, float]:
    """
    Catmull-Rom spline interpolation.

    Args:
        p0, p1, p2, p3: Four control points
        t: Interpolation factor (0-1)

    Returns:
        Interpolated point
    """
    t2 = t * t
    t3 = t2 * t

    # Catmull-Rom basis functions
    q = np.array([
        -0.5 * t3 + t2 - 0.5 * t,
        1.5 * t3 - 2.5 * t2 + 1,
        -1.5 * t3 + 2 * t2 + 0.5 * t,
        0.5 * t3 - 0.5 * t2
    ])

    points = np.array([p0, p1, p2, p3])
    result = q @ points

    return tuple(result)
