"""
Pitch rendering utilities for drawing a realistic football pitch.
"""

import arcade
from typing import Tuple

from ..utils.config import (
    PITCH_COLOR,
    PITCH_LINE_COLOR,
    PITCH_LINE_WIDTH,
    PITCH_LENGTH,
    PITCH_WIDTH
)
from ..utils.coordinate_transform import get_transformer


class PitchRenderer:
    """Renders a football pitch with standard markings."""
    
    def __init__(self):
        """Initialize the pitch renderer."""
        self.transformer = get_transformer()
        self.left, self.right, self.bottom, self.top = self.transformer.get_pitch_bounds()
        
        # Calculate key pitch dimensions in screen space
        self.width = self.right - self.left
        self.height = self.top - self.bottom
        self.center_x = (self.left + self.right) / 2
        self.center_y = (self.bottom + self.top) / 2
        
    def draw(self):
        """Draw the complete pitch with all markings."""
        # Draw grass background
        arcade.draw_rectangle_filled(
            self.center_x,
            self.center_y,
            self.width,
            self.height,
            PITCH_COLOR
        )
        
        # Draw pitch outline
        arcade.draw_rectangle_outline(
            self.center_x,
            self.center_y,
            self.width,
            self.height,
            PITCH_LINE_COLOR,
            border_width=PITCH_LINE_WIDTH
        )
        
        # Draw halfway line
        arcade.draw_line(
            self.center_x,
            self.bottom,
            self.center_x,
            self.top,
            PITCH_LINE_COLOR,
            PITCH_LINE_WIDTH
        )
        
        # Draw center circle
        center_circle_radius = self.transformer.distance_to_pixels(9.15)  # 9.15m radius
        arcade.draw_circle_outline(
            self.center_x,
            self.center_y,
            center_circle_radius,
            PITCH_LINE_COLOR,
            border_width=PITCH_LINE_WIDTH
        )
        
        # Draw center spot
        arcade.draw_circle_filled(
            self.center_x,
            self.center_y,
            self.transformer.distance_to_pixels(0.3),
            PITCH_LINE_COLOR
        )
        
        # Draw penalty areas and goals
        self._draw_penalty_area(left_side=True)
        self._draw_penalty_area(left_side=False)
        
        # Draw goal areas
        self._draw_goal_area(left_side=True)
        self._draw_goal_area(left_side=False)
        
        # Draw corner arcs
        self._draw_corner_arcs()
        
    def _draw_penalty_area(self, left_side: bool):
        """
        Draw penalty area on one side of the pitch.
        
        Args:
            left_side: True for left penalty area, False for right
        """
        # Penalty area is 16.5m deep and 40.3m wide
        depth = self.transformer.distance_to_pixels(16.5)
        width = self.transformer.distance_to_pixels(40.3)
        
        if left_side:
            x_center = self.left + depth / 2
        else:
            x_center = self.right - depth / 2
        
        # Draw penalty area rectangle
        arcade.draw_rectangle_outline(
            x_center,
            self.center_y,
            depth,
            width,
            PITCH_LINE_COLOR,
            border_width=PITCH_LINE_WIDTH
        )
        
        # Draw penalty spot (11m from goal line)
        spot_distance = self.transformer.distance_to_pixels(11.0)
        if left_side:
            spot_x = self.left + spot_distance
        else:
            spot_x = self.right - spot_distance
        
        arcade.draw_circle_filled(
            spot_x,
            self.center_y,
            self.transformer.distance_to_pixels(0.3),
            PITCH_LINE_COLOR
        )
        
        # Draw penalty arc
        arc_radius = self.transformer.distance_to_pixels(9.15)
        if left_side:
            start_angle = -53
            end_angle = 53
        else:
            start_angle = 180 - 53
            end_angle = 180 + 53
        
        arcade.draw_arc_outline(
            spot_x,
            self.center_y,
            arc_radius * 2,
            arc_radius * 2,
            PITCH_LINE_COLOR,
            start_angle,
            end_angle,
            border_width=PITCH_LINE_WIDTH
        )
    
    def _draw_goal_area(self, left_side: bool):
        """
        Draw goal area (6-yard box) on one side.
        
        Args:
            left_side: True for left goal area, False for right
        """
        # Goal area is 5.5m deep and 18.3m wide
        depth = self.transformer.distance_to_pixels(5.5)
        width = self.transformer.distance_to_pixels(18.3)
        
        if left_side:
            x_center = self.left + depth / 2
        else:
            x_center = self.right - depth / 2
        
        arcade.draw_rectangle_outline(
            x_center,
            self.center_y,
            depth,
            width,
            PITCH_LINE_COLOR,
            border_width=PITCH_LINE_WIDTH
        )
    
    def _draw_corner_arcs(self):
        """Draw corner arcs at all four corners."""
        arc_radius = self.transformer.distance_to_pixels(1.0)
        
        # Bottom-left corner
        arcade.draw_arc_outline(
            self.left,
            self.bottom,
            arc_radius * 2,
            arc_radius * 2,
            PITCH_LINE_COLOR,
            0,
            90,
            border_width=PITCH_LINE_WIDTH
        )
        
        # Top-left corner
        arcade.draw_arc_outline(
            self.left,
            self.top,
            arc_radius * 2,
            arc_radius * 2,
            PITCH_LINE_COLOR,
            270,
            360,
            border_width=PITCH_LINE_WIDTH
        )
        
        # Bottom-right corner
        arcade.draw_arc_outline(
            self.right,
            self.bottom,
            arc_radius * 2,
            arc_radius * 2,
            PITCH_LINE_COLOR,
            90,
            180,
            border_width=PITCH_LINE_WIDTH
        )
        
        # Top-right corner
        arcade.draw_arc_outline(
            self.right,
            self.top,
            arc_radius * 2,
            arc_radius * 2,
            PITCH_LINE_COLOR,
            180,
            270,
            border_width=PITCH_LINE_WIDTH
        )