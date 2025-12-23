"""
Ball sprite rendering and physics.

Handles ball visualization, movement interpolation, and physics properties.
"""

import arcade
from typing import Tuple


class BallSprite(arcade.Sprite):
    """Represents the ball in the match replay."""

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        radius: float = 4,
        color: Tuple[int, int, int] = (255, 255, 255)
    ):
        """
        Initialize ball sprite.

        Args:
            x: Initial x position
            y: Initial y position
            radius: Ball radius in pixels
            color: Ball color (RGB)
        """
        super().__init__()
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity_x = 0
        self.velocity_y = 0
        self._create_sprite()

    def _create_sprite(self) -> None:
        """Create ball texture."""
        # Create a simple white circle texture
        texture = arcade.Texture.create_filled(
            f"ball_{self.radius}",
            (int(self.radius * 2), int(self.radius * 2)),
            self.color
        )
        self.texture = texture

    def update_position(
        self,
        x: float,
        y: float,
        velocity_x: float = 0,
        velocity_y: float = 0
    ) -> None:
        """
        Update ball position and velocity.

        Args:
            x: New x position
            y: New y position
            velocity_x: Velocity in x direction
            velocity_y: Velocity in y direction
        """
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def get_position(self) -> Tuple[float, float]:
        """
        Get ball position.

        Returns:
            Tuple of (x, y)
        """
        return (self.x, self.y)

    def get_velocity(self) -> Tuple[float, float]:
        """
        Get ball velocity.

        Returns:
            Tuple of (velocity_x, velocity_y)
        """
        return (self.velocity_x, self.velocity_y)
