# Metrics Reference

## Kinematic Metrics

### Speed
- Instantaneous velocity of a player
- Calculated from position differences between frames
- Units: m/s

### Acceleration
- Rate of change of speed
- Units: m/s²

### Distance Covered
- Total distance traveled by player
- Breakdown by intensity zones:
  - Walking: < 7 km/h
  - Jogging: 7-14 km/h
  - Running: 14-19 km/h
  - Sprinting: > 24 km/h

### Sprint Detection
- Identifies periods of high-speed effort (> 24 km/h)
- Minimum duration: 1 second (10 frames at 10fps)

## Spatial Metrics

### Pitch Control
- Probability of team winning ball at each pitch location
- Based on player proximity and reachability
- 0.5 = equal control, 1.0 = team 1 control, 0.0 = team 2 control

### Convex Hull Area
- Area occupied by team formation
- Larger = more expansive, Smaller = more compact

### Defensive Line Height
- Y-coordinate of deepest defender
- Indicates defensive depth

### Team Compactness
- How tightly grouped a team is
- 0 = completely spread, 1 = all in same position

### Nearest Opponent Distance
- Distance to closest opposing player
- Indicates pressing/isolation

## Tactical Metrics

### Formation
- Detected team shape (4-3-3, 4-4-2, etc.)
- Automatic detection from player positions

### Pressing Intensity
- Aggregate defensiveness of team
- 0 = passive, 1 = maximum pressing

### Pass Completion Rate
- Percentage of passes completed successfully
- By team, player, or time window

## Metrics Computation

All metrics are computed on-demand and cached for performance.
The metrics calculator respects frame ranges for temporal analysis.
