"""
Sprite factory and pool management.

Creates and manages sprite instances for players and ball.
Implements object pooling for performance optimization.
"""

import arcade
from typing import List, Dict, Tuple
from src.sprite.player_sprite import PlayerSprite
from src.sprite.ball_sprite import BallSprite


class SpriteFactory:
    """Creates and manages sprite instances."""

    def __init__(self):
        """Initialize sprite factory."""
        self.player_sprites: List[PlayerSprite] = []
        self.ball_sprite: BallSprite = None
        self.sprite_pool: Dict[str, List[arcade.Sprite]] = {}

    def create_player_sprite(
        self,
        player_id: int,
        team_id: int,
        x: float,
        y: float,
        name: str = "",
        number: int = 0,
        color: Tuple[int, int, int] = (255, 255, 255)
    ) -> PlayerSprite:
        """
        Create a player sprite.

        Args:
            player_id: Player ID
            team_id: Team ID
            x: X position
            y: Y position
            name: Player name
            number: Player jersey number
            color: Team color

        Returns:
            New PlayerSprite instance
        """
        sprite = PlayerSprite(
            player_id=player_id,
            team_id=team_id,
            x=x,
            y=y,
            name=name,
            number=number,
            color=color
        )
        self.player_sprites.append(sprite)
        return sprite

    def create_ball_sprite(
        self,
        x: float = 0,
        y: float = 0
    ) -> BallSprite:
        """
        Create ball sprite.

        Args:
            x: X position
            y: Y position

        Returns:
            BallSprite instance
        """
        self.ball_sprite = BallSprite(x=x, y=y)
        return self.ball_sprite

    def get_all_sprites(self) -> List[arcade.Sprite]:
        """
        Get all active sprites.

        Returns:
            List of all sprites
        """
        sprites = list(self.player_sprites)
        if self.ball_sprite:
            sprites.append(self.ball_sprite)
        return sprites

    def clear_sprites(self) -> None:
        """Clear all sprites."""
        self.player_sprites.clear()
        self.ball_sprite = None

    def reset_sprite_pool(self) -> None:
        """Reset sprite pool."""
        self.sprite_pool.clear()
