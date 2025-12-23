"""
Camera controller for view transforms and zoom.

Manages camera positioning, zoom level, and coordinate transformations.
"""

from typing import Tuple
import numpy as np


class CameraController:
    """Manages camera view and transformations."""

    def __init__(
        self,
        screen_width: float,
        screen_height: float,
        pitch_width: float = 105,
        pitch_height: float = 68
    ):
        """
        Initialize camera controller.

        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
            pitch_width: Pitch width in meters
            pitch_height: Pitch height in meters
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.pitch_width = pitch_width
        self.pitch_height = pitch_height

        self.camera_x = pitch_width / 2
        self.camera_y = pitch_height / 2
        self.zoom = 1.0
        self.ball_lock = False
        self.player_lock_id = None

    def set_position(self, x: float, y: float) -> None:
        """
        Set camera position.

        Args:
            x: Camera center X
            y: Camera center Y
        """
        self.camera_x = max(0, min(x, self.pitch_width))
        self.camera_y = max(0, min(y, self.pitch_height))

    def set_zoom(self, zoom: float) -> None:
        """
        Set zoom level.

        Args:
            zoom: Zoom factor (1.0 = full pitch)
        """
        self.zoom = max(0.5, min(zoom, 3.0))

    def zoom_to_fit_pitch(self) -> None:
        """Zoom to show entire pitch."""
        self.zoom = 1.0
        self.camera_x = self.pitch_width / 2
        self.camera_y = self.pitch_height / 2

    def world_to_screen(
        self,
        world_x: float,
        world_y: float
    ) -> Tuple[float, float]:
        """
        Convert world coordinates to screen coordinates.

        Args:
            world_x: World X coordinate
            world_y: World Y coordinate

        Returns:
            Screen (x, y) coordinates
        """
        # Calculate offset from camera position
        offset_x = world_x - self.camera_x
        offset_y = world_y - self.camera_y

        # Apply zoom
        screen_x = self.screen_width / 2 + offset_x * self.zoom
        screen_y = self.screen_height / 2 + offset_y * self.zoom

        return (screen_x, screen_y)

    def screen_to_world(
        self,
        screen_x: float,
        screen_y: float
    ) -> Tuple[float, float]:
        """
        Convert screen coordinates to world coordinates.

        Args:
            screen_x: Screen X coordinate
            screen_y: Screen Y coordinate

        Returns:
            World (x, y) coordinates
        """
        # Reverse the transformation
        offset_x = (screen_x - self.screen_width / 2) / self.zoom
        offset_y = (screen_y - self.screen_height / 2) / self.zoom

        world_x = self.camera_x + offset_x
        world_y = self.camera_y + offset_y

        return (world_x, world_y)

    def follow_entity(
        self,
        entity_x: float,
        entity_y: float,
        smooth: bool = True
    ) -> None:
        """
        Follow an entity smoothly.

        Args:
            entity_x: Entity X position
            entity_y: Entity Y position
            smooth: Use smooth following
        """
        if smooth:
            self.camera_x += (entity_x - self.camera_x) * 0.1
            self.camera_y += (entity_y - self.camera_y) * 0.1
        else:
            self.set_position(entity_x, entity_y)

    def get_view_matrix(self) -> np.ndarray:
        """
        Get view transformation matrix.

        Returns:
            4x4 view matrix
        """
        # For arcade, we can compute the view bounds
        half_width = self.screen_width / (2 * self.zoom)
        half_height = self.screen_height / (2 * self.zoom)

        left = self.camera_x - half_width
        right = self.camera_x + half_width
        bottom = self.camera_y - half_height
        top = self.camera_y + half_height

        return np.array([
            [2 / (right - left), 0, 0, -(right + left) / (right - left)],
            [0, 2 / (top - bottom), 0, -(top + bottom) / (top - bottom)],
            [0, 0, -1, 0],
            [0, 0, 0, 1]
        ])
