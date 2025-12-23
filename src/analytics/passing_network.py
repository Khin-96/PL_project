"""
Pass network analysis.

Analyzes passing patterns and constructs pass networks.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional


class PassingNetwork:
    """Analyzes passing structure of teams."""

    def __init__(self):
        """Initialize passing network analyzer."""
        self.pass_matrix = None
        self.player_positions = None

    def build_pass_network(
        self,
        passes: List[Dict],
        player_positions: Optional[Dict[int, Tuple[float, float]]] = None
    ) -> Dict:
        """
        Build pass network from pass events.

        Args:
            passes: List of pass events
            player_positions: Optional player positions for network layout

        Returns:
            Network dictionary with nodes and edges
        """
        network = {
            'nodes': [],
            'edges': [],
            'pass_counts': {},
            'success_counts': {}
        }

        if not passes:
            return network

        # Extract unique players
        player_ids = set()
        for pass_event in passes:
            player_ids.add(pass_event.get('player_id'))
            if 'receiver_id' in pass_event:
                player_ids.add(pass_event['receiver_id'])

        # Create nodes
        for i, player_id in enumerate(sorted(player_ids)):
            pos = player_positions.get(player_id, (0, 0)) if player_positions else (0, 0)
            network['nodes'].append({
                'id': player_id,
                'index': i,
                'x': pos[0],
                'y': pos[1]
            })

        # Create edges from passes
        player_to_idx = {n['id']: n['index'] for n in network['nodes']}

        for pass_event in passes:
            passer_id = pass_event.get('player_id')
            receiver_id = pass_event.get('receiver_id')
            successful = pass_event.get('successful', False)

            if passer_id in player_to_idx and receiver_id in player_to_idx:
                passer_idx = player_to_idx[passer_id]
                receiver_idx = player_to_idx[receiver_id]

                # Find existing edge
                edge = None
                for e in network['edges']:
                    if e['source'] == passer_idx and e['target'] == receiver_idx:
                        edge = e
                        break

                if edge:
                    edge['value'] += 1
                    if successful:
                        edge['successful'] += 1
                else:
                    network['edges'].append({
                        'source': passer_idx,
                        'target': receiver_idx,
                        'value': 1,
                        'successful': 1 if successful else 0
                    })

        return network

    def calculate_pass_completion_rate(
        self,
        passes: List[Dict]
    ) -> float:
        """
        Calculate team pass completion rate.

        Args:
            passes: List of pass events

        Returns:
            Completion rate (0-1)
        """
        if not passes:
            return 0.0

        successful = sum(1 for p in passes if p.get('successful', False))
        return successful / len(passes)

    def get_most_connected_player(
        self,
        network: Dict
    ) -> Optional[Dict]:
        """
        Get player with most pass connections.

        Args:
            network: Network dictionary

        Returns:
            Player node or None
        """
        if not network['nodes']:
            return None

        connection_counts = {n['index']: 0 for n in network['nodes']}

        for edge in network['edges']:
            connection_counts[edge['source']] += 1
            connection_counts[edge['target']] += 1

        most_connected_idx = max(connection_counts, key=connection_counts.get)

        for node in network['nodes']:
            if node['index'] == most_connected_idx:
                return node

        return None

    def get_pass_volume(self, network: Dict) -> Dict[int, int]:
        """
        Get pass count for each player.

        Args:
            network: Network dictionary

        Returns:
            Dict mapping player index to pass count
        """
        volumes = {n['index']: 0 for n in network['nodes']}

        for edge in network['edges']:
            volumes[edge['source']] += edge['value']

        return volumes
