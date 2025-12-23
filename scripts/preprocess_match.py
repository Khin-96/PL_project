"""
Data preprocessing and caching script.

Converts JSONL tracking data to cached binary format for faster loading.
"""

import argparse
from pathlib import Path
import numpy as np
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.match_data import MatchData
from src.data.data_cache import DataCache
from src.data.data_validator import DataValidator


def preprocess_match(match_id: str, output_dir: str = "data/processed") -> bool:
    """
    Preprocess a single match.

    Args:
        match_id: Match ID to process
        output_dir: Output directory for cache

    Returns:
        True if successful
    """
    print(f"Processing match {match_id}...")

    try:
        # Load match data
        match = MatchData(match_id=match_id)
        
        # Validate data
        print("Validating data...")
        validator = DataValidator(match.tracking_data, match.metadata)
        is_valid, errors, warnings = validator.validate()

        if errors:
            print("  Errors found:")
            for error in errors:
                print(f"    - {error}")
            return False

        if warnings:
            print("  Warnings:")
            for warning in warnings:
                print(f"    - {warning}")

        # Cache data
        print("Caching data...")
        cache = DataCache(output_dir)

        if match.tracking_data is not None:
            # Extract frame data
            frames = np.arange(len(match.tracking_data))
            success = cache.save_cache(
                int(match_id) if match_id.isdigit() else hash(match_id),
                frames,
                match.tracking_data,
                match.ball_data if hasattr(match, 'ball_data') else None
            )

            if success:
                print(f"  ✓ Match {match_id} cached successfully")
                return True
            else:
                print(f"  ✗ Failed to cache match {match_id}")
                return False
    except Exception as e:
        print(f"  ✗ Error processing match: {e}")
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Preprocess match data and create cached formats"
    )
    parser.add_argument(
        "matches",
        nargs="*",
        help="Match IDs to process (or 'all' for all matches in data/raw/)"
    )
    parser.add_argument(
        "-o", "--output",
        default="data/processed",
        help="Output directory for cached data"
    )

    args = parser.parse_args()

    if not args.matches:
        # Process all matches in data/raw/
        raw_dir = Path("data/raw")
        if not raw_dir.exists():
            print("No data/raw/ directory found")
            return

        tracking_files = list(raw_dir.glob("*_tracking.jsonl"))
        match_ids = [f.stem.replace("_tracking", "") for f in tracking_files]
    else:
        match_ids = args.matches

    if not match_ids:
        print("No matches to process")
        return

    successful = 0
    failed = 0

    for match_id in match_ids:
        if preprocess_match(match_id, args.output):
            successful += 1
        else:
            failed += 1

    print(f"\nResults: {successful} successful, {failed} failed")


if __name__ == "__main__":
    main()
