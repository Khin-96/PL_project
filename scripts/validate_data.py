"""
Data validation script.

Validates tracking data integrity and completeness.
"""

import argparse
from pathlib import Path
import sys
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.data_validator import DataValidator
from src.data.match_data import MatchData


def validate_match(match_id: str) -> bool:
    """
    Validate a single match.

    Args:
        match_id: Match ID to validate

    Returns:
        True if valid
    """
    print(f"\nValidating match {match_id}...")

    try:
        match = MatchData(match_id=match_id)

        if match.tracking_data is None:
            print("  ✗ No tracking data found")
            return False

        validator = DataValidator(match.tracking_data, match.metadata)
        is_valid, errors, warnings = validator.validate()

        if errors:
            print("  ✗ Errors found:")
            for error in errors:
                print(f"    - {error}")

        if warnings:
            print("  ⚠ Warnings:")
            for warning in warnings:
                print(f"    - {warning}")

        if is_valid:
            print(f"  ✓ Match {match_id} is valid")
            return True
        else:
            print(f"  ✗ Match {match_id} has errors")
            return False

    except Exception as e:
        print(f"  ✗ Error validating match: {e}")
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Validate match data")
    parser.add_argument(
        "matches",
        nargs="*",
        help="Match IDs to validate"
    )

    args = parser.parse_args()

    if not args.matches:
        # Validate all matches in data/raw/
        raw_dir = Path("data/raw")
        if not raw_dir.exists():
            print("No data/raw/ directory found")
            return

        tracking_files = list(raw_dir.glob("*_tracking.jsonl"))
        match_ids = [f.stem.replace("_tracking", "") for f in tracking_files]
    else:
        match_ids = args.matches

    if not match_ids:
        print("No matches to validate")
        return

    valid_count = 0
    invalid_count = 0

    for match_id in match_ids:
        if validate_match(match_id):
            valid_count += 1
        else:
            invalid_count += 1

    print(f"\nResults: {valid_count} valid, {invalid_count} invalid")


if __name__ == "__main__":
    main()
