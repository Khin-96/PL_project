# API Reference

## Core Classes

### GameState
Manages current playback state, selections, and display settings.

```python
from src.game_state import GameState

game_state = GameState(match_data, metadata)
game_state.set_current_frame(frame_number)
game_state.select_player(player_id)
game_state.toggle_overlay('heatmap')
```

### MatchData
Loads and provides access to tracking data.

```python
from src.data.match_data import MatchData

match = MatchData(match_id='4039225')
positions = match.get_frame(frame_number)
```

### MetricsCalculator
Computes player and team metrics.

```python
from src.analytics.metrics_calculator import MetricsCalculator

calc = MetricsCalculator(fps=10)
speeds = calc.calculate_speed(position_history)
distance = calc.calculate_distance_covered(position_history)
```

### SpatialAnalyzer
Analyzes team formations and spatial relationships.

```python
from src.analytics.spatial_analyzer import SpatialAnalyzer

analyzer = SpatialAnalyzer()
hull = analyzer.compute_convex_hull(positions)
control = analyzer.compute_pitch_control(team1, team2)
```

### EventManager
Manages match events with temporal indexing.

```python
from src.events.event_manager import EventManager

events = EventManager(event_list)
goal_events = events.get_events_by_type('goal')
next_event = events.get_next_event(current_frame)
```

### CameraController
Manages view transforms and coordinate conversions.

```python
from src.rendering.camera_controller import CameraController

camera = CameraController(screen_width, screen_height)
screen_x, screen_y = camera.world_to_screen(world_x, world_y)
camera.follow_entity(x, y)
```

## Utility Functions

### Coordinate Transformation
```python
from src.utils.coordinates_transform import world_to_screen, screen_to_world

screen_pos = world_to_screen(world_pos, camera_x, camera_y, zoom)
world_pos = screen_to_world(screen_pos, camera_x, camera_y, zoom)
```

### Interpolation
```python
from src.utils.interpolation import cubic_interpolate, linear_interpolate

pos = linear_interpolate(p1, p2, t)
pos = cubic_interpolate(points, t_values, t_target)
```

### Logging
```python
from src.utils.logger import setup_logger, get_logger

logger = setup_logger('module_name')
logger.info("Message")

logger = get_logger('module_name')
```

## Configuration

### Global Settings
```python
from src.utils.config import *

PITCH_WIDTH = 105
PITCH_HEIGHT = 68
FPS_SOURCE = 10
FPS_DISPLAY = 60
```

Modify `src/utils/config.py` to change global parameters.

## Data Validation

```python
from src.data.data_validator import DataValidator

validator = DataValidator(tracking_data, metadata)
is_valid, errors, warnings = validator.validate()
```
