"""
Data validation and integrity checking

Validates tracking data completeness, consistency, and correctness.
Provides detailed error reporting for data issues.
"""

from typing import Dict, List, Tuple
import numpy as np


class DataValidator:
    """Validates tracking data integrity."""

    def __init__(self, tracking_data: np.ndarray, metadata: Dict):
        """
        Initialize validator.

        Args:
            tracking_data: Tracking data array
            metadata: Match metadata
        """
        self.tracking_data = tracking_data
        self.metadata = metadata
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """
        Perform all validation checks.

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []

        self._check_shape()
        self._check_values()
        self._check_continuity()
        self._check_metadata()

        return len(self.errors) == 0, self.errors, self.warnings

    def _check_shape(self) -> None:
        """Validate data shape."""
        if self.tracking_data.ndim != 3:
            self.errors.append(
                f"Expected 3D array, got {self.tracking_data.ndim}D"
            )
        elif self.tracking_data.shape[1] != 23:  # 22 players + ball
            self.warnings.append(
                f"Expected 23 entities, got {self.tracking_data.shape[1]}"
            )

    def _check_values(self) -> None:
        """Validate data values."""
        if np.isnan(self.tracking_data).any():
            nan_count = np.isnan(self.tracking_data).sum()
            self.warnings.append(f"Found {nan_count} NaN values")

        if np.isinf(self.tracking_data).any():
            self.errors.append("Found infinite values")

    def _check_continuity(self) -> None:
        """Check for gaps in frame sequence."""
        if len(self.tracking_data) > 1:
            # Check for missing frames (gaps > 1)
            frame_diffs = np.diff(range(len(self.tracking_data)))
            if (frame_diffs > 1).any():
                gap_count = (frame_diffs > 1).sum()
                self.warnings.append(f"Found {gap_count} gaps in frames")

    def _check_metadata(self) -> None:
        """Validate metadata consistency."""
        if not self.metadata:
            self.warnings.append("No metadata provided")
