"""
Texture cache for rendered overlays.

Caches rendered overlay textures to avoid recomputation.
"""

from typing import Dict, Optional, Tuple
import arcade
import hashlib


class TextureCache:
    """Caches rendered overlay textures."""

    def __init__(self, max_cache_size: int = 100):
        """
        Initialize texture cache.

        Args:
            max_cache_size: Maximum number of cached textures
        """
        self.max_cache_size = max_cache_size
        self.cache: Dict[str, arcade.Texture] = {}
        self.access_count: Dict[str, int] = {}

    def get_key(
        self,
        cache_type: str,
        *args
    ) -> str:
        """
        Generate cache key from parameters.

        Args:
            cache_type: Type of cached item
            args: Arguments to hash

        Returns:
            Cache key string
        """
        key_str = f"{cache_type}:" + "|".join(str(arg) for arg in args)
        return hashlib.md5(key_str.encode()).hexdigest()

    def get(self, key: str) -> Optional[arcade.Texture]:
        """
        Retrieve cached texture.

        Args:
            key: Cache key

        Returns:
            Texture or None if not cached
        """
        if key in self.cache:
            self.access_count[key] = self.access_count.get(key, 0) + 1
            return self.cache[key]
        return None

    def put(self, key: str, texture: arcade.Texture) -> None:
        """
        Cache a texture.

        Args:
            key: Cache key
            texture: Texture to cache
        """
        if len(self.cache) >= self.max_cache_size:
            self._evict_least_used()

        self.cache[key] = texture
        self.access_count[key] = 0

    def clear(self) -> None:
        """Clear entire cache."""
        self.cache.clear()
        self.access_count.clear()

    def _evict_least_used(self) -> None:
        """Remove least recently used texture."""
        if not self.cache:
            return

        least_used_key = min(
            self.access_count.items(),
            key=lambda x: x[1]
        )[0]

        del self.cache[least_used_key]
        del self.access_count[least_used_key]
