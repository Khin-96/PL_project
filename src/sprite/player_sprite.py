"""
Player sprite implementation for rendering and managing individual players.
"""

import arcade
from arcade import draw
from typing import Tuple, Optional
from collections import deque

from utils.config import (
    PLAYER_RADIUS,
    HOME_TEAM_COLOR,
    AWAY_TEAM_COLOR,
    SELECTED_PLAYER_RING_COLOR,
    SELECTED_PLAYER_RING_WIDTH,
    SPEED_SMOOTHING_WINDOW
)
from utils.coordinates_transform import calculate_speed


class PlayerSprite(arcade.Sprite):
    """
    Represents a single player on the pitch.
    Tracks position history and calculates movement metrics.
    """
    
    def __init__(self, player_id: int, team_id: int, jersey_number: int,
                 x: float, y: float, is_home_team: bool = True):
        """
        Initialize a player sprite.
        
        Args:
            player_id: Unique player identifier
            team_id: Team identifier
            jersey_number: Player's jersey number
            x, y: Initial screen coordinates
            is_home_team: True if home team, False if away
        """
        super().__init__()
        
        self.player_id = player_id
        self.team_id = team_id
        self.jersey_number = jersey_number
        self.is_home_team = is_home_team
        self.is_selected = False
        
        # Visual properties
        self.color = HOME_TEAM_COLOR if is_home_team else AWAY_TEAM_COLOR
        self.radius = PLAYER_RADIUS
        
        # Position tracking
        self.center_x = x
        self.center_y = y
        self.position_history = deque(maxlen=SPEED_SMOOTHING_WINDOW)
        self.position_history.append((x, y, 0.0))  # (x, y, timestamp)
        
        # Metrics
        self.current_speed = 0.0  # km/h
        self.total_distance = 0.0  # meters
        self.sprint_distance = 0.0  # meters
        self.last_update_timestamp = 0.0
        
    def update_position(self, x: float, y: float, timestamp: float,
                       raw_x: float, raw_y: float):
        """
        Update player position and recalculate metrics.
        
        Args:
            x, y: New screen coordinates
            timestamp: Current timestamp in seconds
            raw_x, raw_y: Raw pitch coordinates in meters
        """
        # Store previous screen position for distance calculation
        prev_screen_x, prev_screen_y, prev_time = self.position_history[-1]
        
        # Update position
        self.center_x = x
        self.center_y = y
        self.position_history.append((x, y, timestamp))
        
        # Calculate metrics if we have a time delta
        time_delta = timestamp - prev_time
        if time_delta > 0:
            # Calculate speed in km/h
            self.current_speed = calculate_speed(
                prev_screen_x, prev_screen_y,
                x, y,
                time_delta
            )
            
            # Note: This is approximate - for accurate distance we'd need raw coordinates
            # For now, we'll track screen distance as a proxy
            distance_moved = ((x - prev_screen_x) ** 2 + 
                            (y - prev_screen_y) ** 2) ** 0.5
            
            # Convert to meters (rough approximation)
            # This should ideally use raw coordinates
            self.total_distance += distance_moved * 0.01  # Scaling factor
            
            # Track sprint distance
            if self.current_speed > 24.0:  # Sprint threshold
                self.sprint_distance += distance_moved * 0.01
        
        self.last_update_timestamp = timestamp
    
    def draw(self):
        """Custom draw method to render player as a colored circle."""
        # Draw main player circle
        draw.draw_circle_filled(
            self.center_x,
            self.center_y,
            self.radius,
            self.color
        )
        
        # Draw jersey number
        draw.draw_text(
            str(self.jersey_number),
            self.center_x,
            self.center_y - 4,
            arcade.color.WHITE,
            font_size=10,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
        
        # Draw selection ring if selected
        if self.is_selected:
            draw.draw_circle_outline(
                self.center_x,
                self.center_y,
                self.radius + SELECTED_PLAYER_RING_WIDTH,
                SELECTED_PLAYER_RING_COLOR,
                border_width=SELECTED_PLAYER_RING_WIDTH
            )
    
    def get_speed_kmh(self) -> float:
        """Get current speed in km/h."""
        return self.current_speed
    
    def get_distance_covered(self) -> float:
        """Get total distance covered in meters."""
        return self.total_distance
    
    def get_sprint_distance(self) -> float:
        """Get distance covered while sprinting in meters."""
        return self.sprint_distance
    
    def select(self):
        """Mark this player as selected."""
        self.is_selected = True
    
    def deselect(self):
        """Remove selection from this player."""
        self.is_selected = False
    
    def get_metrics_dict(self) -> dict:
        """
        Get all current metrics as a dictionary.
        
        Returns:
            Dictionary of metric names to values
        """
        return {
            'player_id': self.player_id,
            'jersey_number': self.jersey_number,
            'team_id': self.team_id,
            'current_speed_kmh': round(self.current_speed, 2),
            'total_distance_m': round(self.total_distance, 1),
            'sprint_distance_m': round(self.sprint_distance, 1),
            'sprint_percentage': (
                round((self.sprint_distance / self.total_distance * 100), 1)
                if self.total_distance > 0 else 0.0
            )
        }


class BallSprite(arcade.Sprite):
    """Represents the ball."""
    
    def __init__(self, x: float, y: float):
        """
        Initialize ball sprite.
        
        Args:
            x, y: Initial screen coordinates
        """
        super().__init__()
        
        self.center_x = x
        self.center_y = y
        self.z = 0.0  # Height above ground
        
        from utils.config import BALL_RADIUS, BALL_COLOR
        self.radius = BALL_RADIUS
        self.color = BALL_COLOR
        
    def update_position(self, x: float, y: float, z: float = 0.0):
        """
        Update ball position.
        
        Args:
            x, y: New screen coordinates
            z: Height above ground in meters
        """
        self.center_x = x
        self.center_y = y
        self.z = z
    
    def draw(self):
        """Custom draw method to render ball with shadow effect."""
        # Draw shadow if ball is in the air
        if self.z > 0.1:
            shadow_alpha = max(50, min(200, int(255 - self.z * 20)))
            draw.draw_circle_filled(
                self.center_x,
                self.center_y - (self.z * 2),  # Shadow offset
                self.radius * 1.5,
                (*arcade.color.BLACK[:3], shadow_alpha)
            )
        
        # Draw ball
        draw.draw_circle_filled(
            self.center_x,
            self.center_y + (self.z * 2),  # Elevation effect
            self.radius,
            self.color
        )
        
        # Draw highlight for 3D effect
        draw.draw_circle_filled(
            self.center_x - self.radius * 0.3,
            self.center_y + (self.z * 2) + self.radius * 0.3,
            self.radius * 0.4,
            (255, 255, 255, 180)
        )