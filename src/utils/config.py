# Global configuration for the Premier League Replay Engine

# Window settings
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
WINDOW_TITLE = "Premier League Match Replay & Analytics"
FPS_TARGET = 60

# Pitch dimensions (standard FIFA regulations in meters)
PITCH_LENGTH = 105.0
PITCH_WIDTH = 68.0

# Rendering settings
PITCH_COLOR = (34, 139, 34)  # Grass green
PITCH_LINE_COLOR = (255, 255, 255)  # White lines
PITCH_LINE_WIDTH = 2

# Player sprite settings
PLAYER_RADIUS = 8
BALL_RADIUS = 5
HOME_TEAM_COLOR = (220, 20, 60)  # Crimson
AWAY_TEAM_COLOR = (30, 144, 255)  # Dodger blue
BALL_COLOR = (255, 255, 255)  # White
SELECTED_PLAYER_RING_COLOR = (255, 255, 0)  # Yellow
SELECTED_PLAYER_RING_WIDTH = 3

# Performance settings
FRAME_CACHE_SIZE = 300  # Number of frames to pre-load
INTERPOLATION_ENABLED = True
SPATIAL_INDEX_ENABLED = True

# Playback settings
DEFAULT_PLAYBACK_SPEED = 1.0
PLAYBACK_SPEEDS = [0.25, 0.5, 1.0, 2.0, 4.0]
FRAME_SKIP_SECONDS = 5.0

# Data settings
DATA_FPS = 10  # SkillCorner tracking data frequency
RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"
METADATA_DIR = "data/metadata"

# Coordinate transformation
SKILLCORNER_X_MIN = -52.5
SKILLCORNER_X_MAX = 52.5
SKILLCORNER_Y_MIN = -34.0
SKILLCORNER_Y_MAX = 34.0

# UI settings
TIMELINE_HEIGHT = 60
TIMELINE_MARGIN = 20
TELEMETRY_PANEL_WIDTH = 300
TELEMETRY_PANEL_PADDING = 15
UI_BACKGROUND_COLOR = (30, 30, 30, 230)  # Dark gray with transparency
UI_TEXT_COLOR = (255, 255, 255)
UI_FONT_SIZE = 14

# Metric calculation settings
SPEED_SMOOTHING_WINDOW = 5  # Frames to smooth speed calculation
SPRINT_THRESHOLD_KMH = 24.0  # km/h to be considered sprinting
HIGH_INTENSITY_THRESHOLD_KMH = 19.0  # km/h for high intensity running

# Overlay settings
HEATMAP_GRID_SIZE = (21, 14)  # Grid cells for heatmap
HEATMAP_ALPHA = 0.5
PASS_NETWORK_LINE_WIDTH = 2
PASS_NETWORK_MIN_PASSES = 3  # Minimum passes to show connection
FORMATION_LINE_WIDTH = 1
FORMATION_LINE_COLOR = (255, 255, 255, 100)

# Event settings
EVENT_MARKER_RADIUS = 10
EVENT_COLORS = {
    'goal': (255, 215, 0),  # Gold
    'shot': (255, 140, 0),  # Dark orange
    'pass': (173, 216, 230),  # Light blue
    'tackle': (178, 34, 34),  # Firebrick
}

# Debug settings
DEBUG_MODE = False
SHOW_FPS = True
SHOW_FRAME_INFO = False