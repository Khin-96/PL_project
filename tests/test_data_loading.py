"""
Test data loading pipeline.
"""

import sys
from pathlib import Path
import numpy as np
import json
import tempfile

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.data_validator import DataValidator
from src.data.data_cache import DataCache


def test_validator_shape():
    """Test shape validation."""
    # Valid shape: (n_frames, 23 entities, x,y)
    valid_data = np.random.rand(100, 23, 2)
    validator = DataValidator(valid_data, {})
    is_valid, errors, warnings = validator.validate()
    assert is_valid
    print("✓ validator_shape tests passed")


def test_validator_invalid_shape():
    """Test invalid shape detection."""
    invalid_data = np.random.rand(100, 22, 2)  # Should be 23
    validator = DataValidator(invalid_data, {})
    is_valid, errors, warnings = validator.validate()
    assert not is_valid or len(warnings) > 0
    print("✓ validator_invalid_shape tests passed")


def test_cache_save_load():
    """Test cache save and load."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = DataCache(tmpdir)

        # Create test data
        frames = np.arange(100)
        positions = np.random.rand(100, 22, 2) * 105
        ball = np.random.rand(100, 2) * 105

        # Save
        success = cache.save_cache(12345, frames, positions, ball)
        assert success
        print("  ✓ cache save")

        # Load
        loaded = cache.load_cache(12345)
        assert loaded is not None
        loaded_frames, loaded_positions, loaded_ball = loaded
        assert np.allclose(loaded_positions, positions)
        print("  ✓ cache load")

    print("✓ cache tests passed")


def test_cache_clear():
    """Test cache clearing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = DataCache(tmpdir)

        frames = np.arange(100)
        positions = np.random.rand(100, 22, 2)
        ball = np.random.rand(100, 2)

        cache.save_cache(99999, frames, positions, ball)
        assert cache.is_cached(99999)

        cache.clear_cache(99999)
        assert not cache.is_cached(99999)

    print("✓ cache_clear tests passed")


if __name__ == "__main__":
    print("Testing data loading pipeline...\n")
    test_validator_shape()
    test_validator_invalid_shape()
    test_cache_save_load()
    test_cache_clear()
    print("\n✓ All data loading tests passed!")
