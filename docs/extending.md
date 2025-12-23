# Extending the System

## Adding New Visualizations

1. Create a renderer in `src/rendering/`
2. Add methods to `OverlayRenderer` or create new renderer class
3. Update `GameState` to manage new overlay state
4. Add keyboard shortcut to `arcade_replay.py` for toggling

Example: Adding a new visualization overlay
```python
# In overlay_renderer.py
def render_new_overlay(self, data):
    # Compute visualization
    # Render to screen
    pass
```

## Adding New Metrics

1. Create calculator method in `MetricsCalculator` or new analyzer class
2. Update `GameState` to cache computed metric
3. Display in telemetry panel via `UIRenderer`

## Adding New Events

1. Implement detection algorithm in `EventDetector`
2. Register with `EventManager`
3. Add keyboard shortcut for navigation
4. Add visual indicator in overlay

## Data Pipeline Extensions

1. Create loader in `src/data/`
2. Validate with `DataValidator`
3. Cache with `DataCache`
4. Integrate with `match_data.py`

## Common Patterns

### Adding a New Configuration Parameter
```python
# In config.py
NEW_PARAM = 100  # Description

# Usage elsewhere
from src.utils.config import NEW_PARAM
```

### Creating a New Analysis Class
```python
# In appropriate analytics module
class NewAnalyzer:
    def __init__(self):
        pass
    
    def analyze(self, data):
        # Compute result
        return result
```

### Caching Expensive Computations
```python
# In game_state.py
self._cache[cache_key] = expensive_result
```
