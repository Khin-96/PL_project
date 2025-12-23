"""
UI renderer for panels, timeline, and controls.

Renders telemetry panels, timeline scrubber, control hints, and debug info.
"""

import arcade
from typing import Optional, Tuple


class UIRenderer:
    """Renders user interface elements."""

    def __init__(self, width: float, height: float):
        """
        Initialize UI renderer.

        Args:
            width: Screen width
            height: Screen height
        """
        self.width = width
        self.height = height
        self.show_telemetry = True
        self.show_timeline = True
        self.show_controls = True

    def render_telemetry_panel(
        self,
        selected_player: Optional[dict],
        position: Tuple[float, float] = (10, 10)
    ) -> None:
        """
        Render player telemetry panel.

        Args:
            selected_player: Selected player data dict
            position: Top-left position of panel
        """
        if not selected_player or not self.show_telemetry:
            return

        # Draw semi-transparent background panel
        # Render player name, number
        # Render stats: velocity, distance, speed zones, etc.

    def render_timeline(
        self,
        current_frame: int,
        total_frames: int,
        events: list = None,
        position: Tuple[float, float] = None
    ) -> None:
        """
        Render timeline scrubber.

        Args:
            current_frame: Current frame number
            total_frames: Total frames in match
            events: Optional list of events to mark
            position: Bottom position of timeline
        """
        if not self.show_timeline:
            return

        if position is None:
            position = (0, 30)

        # Draw timeline bar
        # Draw current position marker
        # Draw event markers if provided

    def render_control_hints(self) -> None:
        """Render keyboard control hints."""
        if not self.show_controls:
            return

        hints = [
            "SPACE: Pause/Resume",
            "G: Next Goal",
            "H: Toggle Heatmap",
            "P: Pass Network",
            "ESC: Deselect"
        ]

        y_offset = self.height - 20
        for hint in hints:
            # Draw hint text
            y_offset -= 20

    def render_debug_info(
        self,
        fps: float,
        frame_time: float,
        memory_mb: float
    ) -> None:
        """
        Render debug information.

        Args:
            fps: Frames per second
            frame_time: Time per frame in ms
            memory_mb: Memory usage in MB
        """
        debug_text = f"FPS: {fps:.1f} | Frame: {frame_time:.2f}ms | Mem: {memory_mb:.1f}MB"
        # Render debug text in corner

    def render_event_label(
        self,
        event_type: str,
        event_time: str,
        position: Tuple[float, float] = (100, 100)
    ) -> None:
        """
        Render event label overlay.

        Args:
            event_type: Type of event (goal, shot, etc.)
            event_time: Time string (MM:SS)
            position: Screen position
        """
        # Draw event notification overlay
        pass
