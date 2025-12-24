"""
Entry point for the Premier League Match Replay & Analytics Engine.
"""

import arcade
import argparse
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from arcade_replay import MatchReplayWindow
from utils.config import FPS_TARGET


def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        Parsed arguments object
    """
    parser = argparse.ArgumentParser(
        description="Premier League Match Replay & Analytics Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default sample match
  python main.py
  
  # Specify a match ID
  python main.py --match-id 4039225
  
  # Start at first goal
  python main.py --match-id 4039225 --event-type goal --event-index 0
  
  # Enable debug mode
  python main.py --debug
        """
    )
    
    parser.add_argument(
        '--match-id',
        type=str,
        default='4039225',
        help='SkillCorner match identifier (default: 4039225)'
    )
    
    parser.add_argument(
        '--event-type',
        type=str,
        choices=['goal', 'shot', 'pass', 'tackle'],
        help='Jump to first occurrence of this event type'
    )
    
    parser.add_argument(
        '--event-index',
        type=int,
        default=0,
        help='Which occurrence of the event to jump to (0-indexed)'
    )
    
    parser.add_argument(
        '--start-time',
        type=float,
        help='Start playback at specific timestamp (seconds)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode with performance metrics'
    )
    
    parser.add_argument(
        '--fps',
        type=int,
        default=FPS_TARGET,
        help=f'Target frames per second (default: {FPS_TARGET})'
    )
    
    return parser.parse_args()


def validate_data_files(match_id: str) -> bool:
    """
    Check if required data files exist for the match.
    
    Args:
        match_id: Match identifier to validate
        
    Returns:
        True if files exist, False otherwise
    """
    from utils.config import RAW_DATA_DIR
    
    raw_dir = Path(RAW_DATA_DIR)
    
    # Check for either raw files or cached data
    tracking_file = raw_dir / f"{match_id}_tracking_extrapolated.jsonl"
    metadata_file = raw_dir / f"{match_id}_match.json"
    
    if not tracking_file.exists() and not metadata_file.exists():
        print(f"Error: No data files found for match {match_id}")
        print(f"Expected files in {raw_dir}:")
        print(f"  - {match_id}_tracking_extrapolated.jsonl")
        print(f"  - {match_id}_match.json")
        print()
        print("To download sample data, run:")
        print("  python scripts/download_sample_data.py")
        return False
    
    return True


def main():
    """Main entry point."""
    args = parse_arguments()
    
    print("=" * 60)
    print("Premier League Match Replay & Analytics Engine")
    print("=" * 60)
    print()
    
    # Validate data exists
    if not validate_data_files(args.match_id):
        sys.exit(1)
    
    # Set debug mode if requested
    if args.debug:
        from utils.config import DEBUG_MODE
        DEBUG_MODE = True
        print("Debug mode enabled")
    
    try:
        # Create and setup window
        print(f"Initializing replay for match {args.match_id}...")
        window = MatchReplayWindow(args.match_id)
        window.setup()
        
        # Handle start position
        if args.start_time is not None:
            print(f"Seeking to {args.start_time:.1f} seconds...")
            window.game_state.seek_to_timestamp(args.start_time)
        
        elif args.event_type is not None:
            # This would require event data loading
            # For now, just inform the user
            print(f"Event navigation ({args.event_type}) not yet implemented")
            print("Starting from beginning...")
        
        # Print match info
        metadata = window.game_state.get_metadata()
        if metadata:
            home_team = metadata.get('home_team', {}).get('name', 'Unknown')
            away_team = metadata.get('away_team', {}).get('name', 'Unknown')
            print()
            print(f"Match: {home_team} vs {away_team}")
            print(f"Duration: {window.game_state.format_time(window.game_state.get_total_duration())}")
            print(f"Total frames: {window.game_state.get_total_frames()}")
        
        print()
        print("Starting replay...")
        print("Press SPACE to pause, 1-4 for playback speed")
        print("Click any player to see their stats")
        print()
        
        # Run the game
        arcade.run()
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Make sure you've downloaded the match data first.")
        sys.exit(1)
    
    except KeyboardInterrupt:
        print()
        print("Replay interrupted by user")
        sys.exit(0)
    
    except Exception as e:
        print(f"Fatal error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()