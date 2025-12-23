"""
Coordinate transformation utilities for converting SkillCorner coordinates
to screen space and handling pitch geometry.
"""

from typing import Tuple
from .config import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    SKILLCORNER_X_MIN, SKILLCORNER_X_MAX,
    SKILLCORNER_Y_MIN, SKILLCORNER_Y_MAX,
    PITCH_LENGTH, PITCH_WIDTH
)


class CoordinateTransformer:
    """Handles all coordinate system transformations."""
    
    def __init__(self, pitch_margin: int = 50):
        """
        Initialize the transformer with screen dimensions and margins.
        
        Args:
            pitch_margin: Pixels of margin around the pitch
        """
        self.pitch_margin = pitch_margin
        self.pitch_screen_width = WINDOW_WIDTH - (2 * pitch_margin)
        self.pitch_screen_height = WINDOW_HEIGHT - (2 * pitch_margin) - 100  # Extra for UI
        
        # Calculate scaling factors
        self.x_scale = self.pitch_screen_width / PITCH_LENGTH
        self.y_scale = self.pitch_screen_height / PITCH_WIDTH
        
    def skillcorner_to_screen(self, x: float, y: float) -> Tuple[float, float]:
        """
        Convert SkillCorner coordinates (meters from center) to screen pixels.
        
        SkillCorner format:
        - Origin (0, 0) is at pitch center
        - X axis: -52.5 to +52.5 (105m pitch)
        - Y axis: -34 to +34 (68m pitch)
        
        Args:
            x: X coordinate in meters from center
            y: Y coordinate in meters from center
            
        Returns:
            Tuple of (screen_x, screen_y) in pixels
        """
        # Normalize to 0-1 range
        normalized_x = (x - SKILLCORNER_X_MIN) / PITCH_LENGTH
        normalized_y = (y - SKILLCORNER_Y_MIN) / PITCH_WIDTH
        
        # Scale to screen space and add margin
        screen_x = (normalized_x * self.pitch_screen_width) + self.pitch_margin
        screen_y = (normalized_y * self.pitch_screen_height) + self.pitch_margin
        
        return screen_x, screen_y
    
    def screen_to_skillcorner(self, screen_x: float, screen_y: float) -> Tuple[float, float]:
        """
        Convert screen pixels back to SkillCorner coordinates.
        Useful for click detection and spatial queries.
        
        Args:
            screen_x: X coordinate in pixels
            screen_y: Y coordinate in pixels
            
        Returns:
            Tuple of (x, y) in meters from pitch center
        """
        # Remove margin and normalize
        normalized_x = (screen_x - self.pitch_margin) / self.pitch_screen_width
        normalized_y = (screen_y - self.pitch_margin) / self.pitch_screen_height
        
        # Scale to SkillCorner range
        x = (normalized_x * PITCH_LENGTH) + SKILLCORNER_X_MIN
        y = (normalized_y * PITCH_WIDTH) + SKILLCORNER_Y_MIN
        
        return x, y
    
    def distance_to_pixels(self, meters: float) -> float:
        """
        Convert a distance in meters to screen pixels.
        Uses average of x and y scales.
        
        Args:
            meters: Distance in meters
            
        Returns:
            Distance in pixels
        """
        avg_scale = (self.x_scale + self.y_scale) / 2
        return meters * avg_scale
    
    def get_pitch_bounds(self) -> Tuple[float, float, float, float]:
        """
        Get the screen coordinates of the pitch boundaries.
        
        Returns:
            Tuple of (left, right, bottom, top) in screen pixels
        """
        left = self.pitch_margin
        right = self.pitch_margin + self.pitch_screen_width
        bottom = self.pitch_margin
        top = self.pitch_margin + self.pitch_screen_height
        
        return left, right, bottom, top
    
    def is_on_pitch(self, x: float, y: float) -> bool:
        """
        Check if SkillCorner coordinates are within pitch boundaries.
        
        Args:
            x: X coordinate in meters
            y: Y coordinate in meters
            
        Returns:
            True if position is on the pitch
        """
        return (SKILLCORNER_X_MIN <= x <= SKILLCORNER_X_MAX and
                SKILLCORNER_Y_MIN <= y <= SKILLCORNER_Y_MAX)


# Global transformer instance
_transformer = None


def get_transformer(reset: bool = False) -> CoordinateTransformer:
    """
    Get or create the global coordinate transformer instance.
    
    Args:
        reset: If True, create a new transformer instance
        
    Returns:
        CoordinateTransformer instance
    """
    global _transformer
    if _transformer is None or reset:
        _transformer = CoordinateTransformer()
    return _transformer


def meters_per_second_to_kmh(mps: float) -> float:
    """Convert meters per second to kilometers per hour."""
    return mps * 3.6


def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Calculate Euclidean distance between two points.
    
    Args:
        x1, y1: First point coordinates
        x2, y2: Second point coordinates
        
    Returns:
        Distance in meters
    """
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def calculate_speed(x1: float, y1: float, x2: float, y2: float, time_delta: float) -> float:
    """
    Calculate speed between two positions.
    
    Args:
        x1, y1: Starting position in meters
        x2, y2: Ending position in meters
        time_delta: Time elapsed in seconds
        
    Returns:
        Speed in km/h
    """
    if time_delta == 0:
        return 0.0
    
    distance = calculate_distance(x1, y1, x2, y2)
    mps = distance / time_delta
    return meters_per_second_to_kmh(mps)