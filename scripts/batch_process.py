"""
Batch processing script.

Process multiple matches in parallel.
"""

import argparse
from pathlib import Path
import sys
import multiprocessing as mp

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.data_cache import DataCache
from src.data.match_data import MatchData


def process_match(match_id: str, output_dir: str = "data/processed"):
    """
    Process a single match (for parallel execution).

    Args:
        match_id: Match ID
        output_dir: Output directory
    """
    try:
        match = MatchData(match_id=match_id)
        cache = DataCache(output_dir)

        if match.tracking_data is not None:
            cache.save_cache(
                int(match_id) if match_id.isdigit() else hash(match_id),
                None,
                match.tracking_data,
                None
            )
            print(f"✓ {match_id}")
            return True
    except Exception as e:
        print(f"✗ {match_id}: {e}")
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Process multiple matches in parallel"
    )
    parser.add_argument(
        "matches",
        nargs="*",
        help="Match IDs to process"
    )
    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=mp.cpu_count(),
        help="Number of parallel workers"
    )
    parser.add_argument(
        "-o", "--output",
        default="data/processed",
        help="Output directory"
    )

    args = parser.parse_args()

    if not args.matches:
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

    print(f"Processing {len(match_ids)} matches with {args.workers} workers...")

    with mp.Pool(args.workers) as pool:
        results = [
            pool.apply_async(process_match, (m_id, args.output))
            for m_id in match_ids
        ]

        successful = sum(1 for r in results if r.get(timeout=300))
        print(f"\nCompleted: {successful}/{len(match_ids)} matches")


if __name__ == "__main__":
    main()
