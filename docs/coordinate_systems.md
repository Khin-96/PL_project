# Coordinate Systems

## Pitch Coordinates

The standard pitch coordinate system:
- Width: 105 meters
- Height: 68 meters
- Origin: Bottom-left corner
- X-axis: 0-105 (goal lines)
- Y-axis: 0-68 (sidelines)

## Screen Coordinates

Screen coordinates depend on viewport:
- Origin: Top-left corner of window
- X-axis: 0 to window width (left to right)
- Y-axis: 0 to window height (top to bottom)

## Coordinate Transformations

World coordinates → Screen coordinates:
```
offset_x = world_x - camera_x
offset_y = world_y - camera_y
screen_x = window_center_x + offset_x * zoom
screen_y = window_center_y + offset_y * zoom
```

Screen coordinates → World coordinates (inverse):
```
offset_x = (screen_x - window_center_x) / zoom
offset_y = (screen_y - window_center_y) / zoom
world_x = camera_x + offset_x
world_y = camera_y + offset_y
```

## Camera and View Management

The `CameraController` class handles all coordinate transformations, zoom levels, and view following.
