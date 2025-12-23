"""
Event context windows.

Provides context windows around events for narrative replay.
"""

from typing import Dict, List, Tuple, Optional


class EventContext:
    """Manages context windows around events."""

    def __init__(
        self,
        default_before_frames: int = 150,  # 15 seconds at 10fps
        default_after_frames: int = 50     # 5 seconds at 10fps
    ):
        """
        Initialize event context manager.

        Args:
            default_before_frames: Default frames to show before event
            default_after_frames: Default frames to show after event
        """
        self.default_before = default_before_frames
        self.default_after = default_after_frames

    def get_context_window(
        self,
        event: Dict,
        total_frames: int,
        before: Optional[int] = None,
        after: Optional[int] = None
    ) -> Tuple[int, int]:
        """
        Get context window frame range for event.

        Args:
            event: Event dictionary with 'frame' key
            total_frames: Total frames in match
            before: Override default before frames
            after: Override default after frames

        Returns:
            (start_frame, end_frame) tuple
        """
        event_frame = event.get('frame', 0)
        before_frames = before if before is not None else self.default_before
        after_frames = after if after is not None else self.default_after

        start_frame = max(0, event_frame - before_frames)
        end_frame = min(total_frames - 1, event_frame + after_frames)

        return (start_frame, end_frame)

    def get_buildup_context(
        self,
        event: Dict,
        total_frames: int,
        buildup_frames: int = 300  # 30 seconds
    ) -> Tuple[int, int]:
        """
        Get context window showing buildup to event.

        Args:
            event: Event dictionary
            total_frames: Total frames
            buildup_frames: How many frames before event

        Returns:
            (start_frame, end_frame) tuple
        """
        event_frame = event.get('frame', 0)
        start_frame = max(0, event_frame - buildup_frames)
        end_frame = event_frame

        return (start_frame, end_frame)

    def get_reaction_context(
        self,
        event: Dict,
        total_frames: int,
        reaction_frames: int = 150  # 15 seconds
    ) -> Tuple[int, int]:
        """
        Get context window showing reaction after event.

        Args:
            event: Event dictionary
            total_frames: Total frames
            reaction_frames: How many frames after event

        Returns:
            (start_frame, end_frame) tuple
        """
        event_frame = event.get('frame', 0)
        start_frame = event_frame
        end_frame = min(total_frames - 1, event_frame + reaction_frames)

        return (start_frame, end_frame)

    def get_sequence_context(
        self,
        start_event: Dict,
        end_event: Dict,
        total_frames: int,
        padding: int = 50
    ) -> Tuple[int, int]:
        """
        Get context for sequence between two events.

        Args:
            start_event: First event
            end_event: Last event
            total_frames: Total frames
            padding: Extra frames before/after

        Returns:
            (start_frame, end_frame) tuple
        """
        start_frame = max(0, start_event.get('frame', 0) - padding)
        end_frame = min(total_frames - 1, end_event.get('frame', 0) + padding)

        return (start_frame, end_frame)

    def get_related_events(
        self,
        event: Dict,
        all_events: List[Dict],
        frame_window: int = 300
    ) -> List[Dict]:
        """
        Get events related to a specific event.

        Args:
            event: Event of interest
            all_events: All available events
            frame_window: Time window to search

        Returns:
            List of related events
        """
        event_frame = event.get('frame', 0)
        related = []

        for other_event in all_events:
            other_frame = other_event.get('frame', 0)
            if abs(other_frame - event_frame) <= frame_window:
                if other_event != event:
                    related.append(other_event)

        return related
