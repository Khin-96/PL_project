"""
Event data loading and management.

Handles parsing SkillCorner dynamic events CSV files and provides
structured access to event data (goals, shots, passes, etc.).
"""

import pandas as pd
from typing import List, Dict, Optional, Tuple
from pathlib import Path


class EventData:
    """Loads and manages match event data."""

    def __init__(self, csv_path: str):
        """
        Initialize event data loader.

        Args:
            csv_path: Path to SkillCorner events CSV file
        """
        self.csv_path = Path(csv_path)
        self.events_df = None
        self._load_events()

    def _load_events(self) -> None:
        """Load events from CSV file."""
        if self.csv_path.exists():
            self.events_df = pd.read_csv(self.csv_path)
        else:
            self.events_df = pd.DataFrame()

    def get_events_by_type(self, event_type: str) -> List[Dict]:
        """
        Get all events of a specific type.

        Args:
            event_type: Type of event (e.g., 'goal', 'shot', 'pass')

        Returns:
            List of event dictionaries
        """
        if self.events_df.empty:
            return []
        filtered = self.events_df[self.events_df['type'] == event_type]
        return filtered.to_dict('records')

    def get_events_in_timeframe(
        self,
        start_frame: int,
        end_frame: int
    ) -> List[Dict]:
        """
        Get all events within a frame range.

        Args:
            start_frame: Starting frame number
            end_frame: Ending frame number

        Returns:
            List of event dictionaries
        """
        if self.events_df.empty:
            return []
        filtered = self.events_df[
            (self.events_df['frame'] >= start_frame) &
            (self.events_df['frame'] <= end_frame)
        ]
        return filtered.to_dict('records')

    def get_next_event(
        self,
        current_frame: int,
        event_type: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Get the next event after current frame.

        Args:
            current_frame: Current frame number
            event_type: Optional filter by event type

        Returns:
            Next event dict or None
        """
        if self.events_df.empty:
            return None

        filtered = self.events_df[self.events_df['frame'] > current_frame]
        if event_type:
            filtered = filtered[filtered['type'] == event_type]

        if filtered.empty:
            return None

        return filtered.iloc[0].to_dict()

    def get_previous_event(
        self,
        current_frame: int,
        event_type: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Get the previous event before current frame.

        Args:
            current_frame: Current frame number
            event_type: Optional filter by event type

        Returns:
            Previous event dict or None
        """
        if self.events_df.empty:
            return None

        filtered = self.events_df[self.events_df['frame'] < current_frame]
        if event_type:
            filtered = filtered[filtered['type'] == event_type]

        if filtered.empty:
            return None

        return filtered.iloc[-1].to_dict()
