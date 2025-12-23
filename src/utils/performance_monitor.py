"""
Performance monitoring and profiling.

Tracks FPS, frame time, memory usage, and other performance metrics.
"""

import time
import psutil
import os
from typing import Dict, Optional
from collections import deque


class PerformanceMonitor:
    """Monitors application performance metrics."""

    def __init__(self, max_history: int = 120):
        """
        Initialize performance monitor.

        Args:
            max_history: Maximum frames to keep in history
        """
        self.max_history = max_history
        self.frame_times = deque(maxlen=max_history)
        self.fps_history = deque(maxlen=max_history)

        self.last_frame_time = time.time()
        self.process = psutil.Process(os.getpid())

    def update(self) -> None:
        """Record frame time."""
        current_time = time.time()
        frame_time = current_time - self.last_frame_time
        self.frame_times.append(frame_time)

        if frame_time > 0:
            fps = 1.0 / frame_time
        else:
            fps = 0

        self.fps_history.append(fps)
        self.last_frame_time = current_time

    def get_fps(self) -> float:
        """Get current FPS."""
        if not self.fps_history:
            return 0.0
        return self.fps_history[-1]

    def get_average_fps(self) -> float:
        """Get average FPS over history."""
        if not self.fps_history:
            return 0.0
        return sum(self.fps_history) / len(self.fps_history)

    def get_frame_time_ms(self) -> float:
        """Get current frame time in milliseconds."""
        if not self.frame_times:
            return 0.0
        return self.frame_times[-1] * 1000

    def get_average_frame_time_ms(self) -> float:
        """Get average frame time in milliseconds."""
        if not self.frame_times:
            return 0.0
        return sum(self.frame_times) / len(self.frame_times) * 1000

    def get_memory_usage_mb(self) -> float:
        """Get memory usage in MB."""
        try:
            mem_info = self.process.memory_info()
            return mem_info.rss / (1024 * 1024)
        except Exception:
            return 0.0

    def get_metrics(self) -> Dict[str, float]:
        """
        Get all performance metrics.

        Returns:
            Dictionary of metrics
        """
        return {
            'current_fps': self.get_fps(),
            'average_fps': self.get_average_fps(),
            'frame_time_ms': self.get_frame_time_ms(),
            'average_frame_time_ms': self.get_average_frame_time_ms(),
            'memory_mb': self.get_memory_usage_mb(),
        }

    def reset(self) -> None:
        """Reset metrics."""
        self.frame_times.clear()
        self.fps_history.clear()
        self.last_frame_time = time.time()
