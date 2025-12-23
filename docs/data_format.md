# Data Format Specification

## SkillCorner Tracking Data Format

Tracking data from SkillCorner is provided in JSONL (JSON Lines) format, where each line represents one frame of tracking data.

### Frame Structure

Each frame contains:
- Timestamp
- Ball position (x, y)
- Player positions (22 players, 11 per team)
- Optional: ball possession information

### Coordinate System

- X-axis: 0-105 meters (goal lines)
- Y-axis: 0-68 meters (sidelines)
- Origin (0, 0): Bottom-left corner (defending goal for team 1)

### Data Validation

All tracking data is validated for:
- Shape consistency (22 players + ball)
- Value ranges (within pitch boundaries)
- Continuity (no unexplained gaps)
- Realistic movement (no infinite velocities)

## Event Data Format

Event data is provided in CSV format with columns:
- frame: Frame number
- type: Event type (goal, shot, pass, etc.)
- player_id: Player making the action
- x, y: Position of event
- additional fields depending on event type

## Metadata Format

Match metadata in JSON format includes:
- match_id, date, teams, players
- Team information (team_id, name, formation)
- Player information (player_id, name, number, position)
