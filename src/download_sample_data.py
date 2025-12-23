"""
Download sample tracking data from SkillCorner's open dataset.
"""

import os
import sys
import requests
from pathlib import Path
from urllib.parse import urljoin


# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config import RAW_DATA_DIR


# SkillCorner open data repository
SKILLCORNER_BASE_URL = "https://raw.githubusercontent.com/SkillCorner/opendata/master/"

# Sample matches to download
SAMPLE_MATCHES = [
    {
        'id': '4039225',
        'description': 'A-League 2024/25 Sample Match',
        'files': [
            'match_data/4039225_match.json',
            'match_data/4039225_tracking_extrapolated.jsonl'
        ]
    }
]


def download_file(url: str, destination: Path) -> bool:
    """
    Download a file from URL to destination.
    
    Args:
        url: Source URL
        destination: Target file path
        
    Returns:
        True if successful
    """
    try:
        print(f"  Downloading: {url}")
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Create parent directories if needed
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"  Saved to: {destination}")
        return True
        
    except requests.RequestException as e:
        print(f"  Error downloading: {e}")
        return False


def main():
    """Download all sample matches."""
    print("SkillCorner Open Data Downloader")
    print("=" * 60)
    print()
    
    raw_dir = Path(RAW_DATA_DIR)
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Download directory: {raw_dir}")
    print()
    
    total_files = sum(len(match['files']) for match in SAMPLE_MATCHES)
    downloaded = 0
    failed = 0
    
    for match in SAMPLE_MATCHES:
        print(f"Match {match['id']}: {match['description']}")
        print("-" * 60)
        
        for file_path in match['files']:
            # Construct URL
            url = urljoin(SKILLCORNER_BASE_URL, file_path)
            
            # Determine local filename
            filename = os.path.basename(file_path)
            destination = raw_dir / filename
            
            # Skip if already exists
            if destination.exists():
                print(f"  Already exists: {filename}")
                downloaded += 1
                continue
            
            # Download
            if download_file(url, destination):
                downloaded += 1
            else:
                failed += 1
        
        print()
    
    # Summary
    print("=" * 60)
    print(f"Download complete!")
    print(f"  Total files: {total_files}")
    print(f"  Downloaded: {downloaded}")
    print(f"  Failed: {failed}")
    print()
    
    if failed > 0:
        print("Some files failed to download.")
        print("You can try running this script again.")
        return 1
    
    print("All sample data downloaded successfully!")
    print()
    print("To start the replay, run:")
    print("  python src/main.py")
    print()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())