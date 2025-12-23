"""
Test coordinate transformations.
"""

import sys
from pathlib import Path
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rendering.camera_controller import CameraController


def test_world_to_screen():
    """Test world to screen conversion."""
    camera = CameraController(800, 600, 105, 68)

    # Center of pitch to center of screen
    screen_x, screen_y = camera.world_to_screen(52.5, 34)
    assert abs(screen_x - 400) < 1
    assert abs(screen_y - 300) < 1
    print("✓ world_to_screen: center")

    # Corner
    camera.zoom = 1.0
    screen_x, screen_y = camera.world_to_screen(0, 0)
    print(f"  Corner (0,0) -> screen ({screen_x}, {screen_y})")

    print("✓ world_to_screen tests passed")


def test_screen_to_world():
    """Test screen to world conversion."""
    camera = CameraController(800, 600, 105, 68)

    # Center of screen to center of pitch
    world_x, world_y = camera.screen_to_world(400, 300)
    assert abs(world_x - 52.5) < 1
    assert abs(world_y - 34) < 1
    print("✓ screen_to_world: center")

    print("✓ screen_to_world tests passed")


def test_zoom():
    """Test zoom functionality."""
    camera = CameraController(800, 600, 105, 68)

    # Original zoom
    screen_x1, screen_y1 = camera.world_to_screen(52.5, 34)

    # Zoom in
    camera.set_zoom(2.0)
    screen_x2, screen_y2 = camera.world_to_screen(52.5, 34)

    # Zoomed position should be further from screen center
    assert abs(screen_x1 - screen_x2) < 0.1  # Still same point
    print("✓ zoom tests passed")


def test_follow():
    """Test camera following."""
    camera = CameraController(800, 600, 105, 68)
    initial_x, initial_y = camera.camera_x, camera.camera_y

    # Follow entity
    camera.follow_entity(70, 50, smooth=True)
    assert camera.camera_x > initial_x
    assert camera.camera_y > initial_y
    print("✓ follow tests passed")


if __name__ == "__main__":
    print("Testing coordinate transformations...\n")
    test_world_to_screen()
    test_screen_to_world()
    test_zoom()
    test_follow()
    print("\n✓ All coordinate transformation tests passed!")
