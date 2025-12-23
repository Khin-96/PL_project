"""
Event management and indexing.

Provides efficient access to match events with temporal indexing.
"""

from typing import List, Dict, Optional, Tuple
import numpy as np


class EventManager:
    """Manages match events with efficient temporal indexing."""

    def __init__(self, events: Optional[List[Dict]] = None):
        """
        Initialize event manager.

        Args:
            events: Optional list of event dictionaries
        """
        self.events = events or []
        self._build_index()

    def _build_index(self) -> None:
        """Build temporal index for fast lookups."""
        if not self.events:
            self.frame_index = {}
            self.type_index = {}
            return

        # Index by frame
        self.frame_index = {}
        for i, event in enumerate(self.events):
            frame = event.get('frame', 0)
            if frame not in self.frame_index:
                self.frame_index[frame] = []
            self.frame_index[frame].append(i)

        # Index by type
        self.type_index = {}
        for i, event in enumerate(self.events):
            event_type = event.get('type', 'unknown')
            if event_type not in self.type_index:
                self.type_index[event_type] = []
            self.type_index[event_type].append(i)

    def add_event(self, event: Dict) -> None:
        """
        Add an event.

        Args:
            event: Event dictionary
        """
        self.events.append(event)
        self._build_index()

    def get_events_at_frame(self, frame: int) -> List[Dict]:
        """
        Get events at specific frame.

        Args:
            frame: Frame number

        Returns:
            List of events
        """
        if frame not in self.frame_index:
            return []

        indices = self.frame_index[frame]
        return [self.events[i] for i in indices]

    def get_events_by_type(self, event_type: str) -> List[Dict]:
        """
        Get all events of specific type.

        Args:
            event_type: Event type

        Returns:
            List of events
        """
        if event_type not in self.type_index:
            return []

        indices = self.type_index[event_type]
        return [self.events[i] for i in indices]

    def get_next_event(
        self,
        current_frame: int,
        event_type: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Get next event after frame.

        Args:
            current_frame: Starting frame
            event_type: Optional filter by type

        Returns:
            Next event or None
        """
        candidates = []

        if event_type:
            indices = self.type_index.get(event_type, [])
            candidates = [self.events[i] for i in indices]
        else:
            candidates = self.events

        for event in candidates:
            if event.get('frame', 0) > current_frame:
                return event

        return None

    def get_previous_event(
        self,
        current_frame: int,
        event_type: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Get previous event before frame.

        Args:
            current_frame: Starting frame
            event_type: Optional filter by type

        Returns:
            Previous event or None
        """
        candidates = []

        if event_type:
            indices = self.type_index.get(event_type, [])
            candidates = [self.events[i] for i in indices]
        else:
            candidates = self.events

        result = None
        for event in candidates:
            if event.get('frame', 0) < current_frame:
                result = event

        return result
