"""
Match metadata loading.

Loads and manages match metadata including team info, player rosters,
and match-level information.
"""

import json
from typing import Dict, Optional, List
from pathlib import Path


class MetadataLoader:
    """Loads and provides access to match metadata."""

    def __init__(self, metadata_path: str):
        """
        Initialize metadata loader.

        Args:
            metadata_path: Path to metadata JSON file
        """
        self.metadata_path = Path(metadata_path)
        self.metadata: Dict = {}
        self._load_metadata()

    def _load_metadata(self) -> None:
        """Load metadata from JSON file."""
        if self.metadata_path.exists():
            with open(self.metadata_path, 'r') as f:
                self.metadata = json.load(f)

    def get_match_info(self) -> Dict:
        """Get match-level information."""
        return self.metadata.get('match', {})

    def get_team_info(self, team_id: Optional[int] = None) -> Dict:
        """
        Get team information.

        Args:
            team_id: Optional specific team ID

        Returns:
            Team info dictionary
        """
        teams = self.metadata.get('teams', [])
        if team_id:
            for team in teams:
                if team.get('team_id') == team_id:
                    return team
        return teams[0] if teams else {}

    def get_players(self, team_id: Optional[int] = None) -> List[Dict]:
        """
        Get player information.

        Args:
            team_id: Optional filter by team ID

        Returns:
            List of player dictionaries
        """
        players = self.metadata.get('players', [])
        if team_id:
            return [p for p in players if p.get('team_id') == team_id]
        return players

    def get_player_by_id(self, player_id: int) -> Optional[Dict]:
        """
        Get specific player information.

        Args:
            player_id: Player ID

        Returns:
            Player dictionary or None
        """
        for player in self.metadata.get('players', []):
            if player.get('player_id') == player_id:
                return player
        return None
