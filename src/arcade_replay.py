"""
Main Arcade window and game loop for the Premier League Replay system.
"""

import arcade
from typing import Dict, Optional

from .game_state import GameState
from .rendering.pitch_renderer import PitchRenderer
from .sprites.player_sprite import PlayerSprite, BallSprite
from .utils.coordinate_transform import get_transformer
from .utils.config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    FPS_TARGET,
    UI_BACKGROUND_COLOR,
    UI_TEXT_COLOR,
    UI_FONT_SIZE,
    TIMELINE_HEIGHT,
    TIMELINE_MARGIN,
    TELEMETRY_PANEL_WIDTH,
    TELEMETRY_PANEL_PADDING,
    FRAME_SKIP_SECONDS,
    DATA_FPS
)


class MatchReplayWindow(arcade.Window):
    """Main application window for match replay."""
    
    def __init__(self, match_id: str):
        """
        Initialize the replay window.
        
        Args:
            match_id: SkillCorner match identifier
        """
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        
        arcade.set_background_color(arcade.color.BLACK)
        
        # Initialize game state
        self.game_state = GameState(match_id)
        
        # Initialize renderers
        self.pitch_renderer = PitchRenderer()
        self.transformer = get_transformer()
        
        # Sprite management
        self.player_sprites: Dict[int, PlayerSprite] = {}
        self.ball_sprite: Optional[BallSprite] = None
        
        # Input state
        self.mouse_x = 0
        self.mouse_y = 0
        
        # Performance tracking
        self.fps_history = []
        
        print("Replay window initialized successfully")
    
    def setup(self):
        """Set up the game - create initial sprites."""
        # Create initial sprites from first frame
        frame = self.game_state.get_current_frame()
        if frame:
            self._create_sprites_from_frame(frame)
    
    def _create_sprites_from_frame(self, frame):
        """
        Create or update sprites based on frame data.
        
        Args:
            frame: MatchFrame object with player and ball positions
        """
        # Get metadata to determine home/away teams
        metadata = self.game_state.get_metadata()
        home_team_id = metadata.get('home_team', {}).get('id', 0)
        
        # Update or create player sprites
        existing_player_ids = set(self.player_sprites.keys())
        current_player_ids = set()
        
        for player in frame.players:
            current_player_ids.add(player.player_id)
            
            # Convert to screen coordinates
            screen_x, screen_y = self.transformer.skillcorner_to_screen(
                player.x, player.y
            )
            
            # Create or update sprite
            if player.player_id not in self.player_sprites:
                is_home = (player.team_id == home_team_id)
                sprite = PlayerSprite(
                    player.player_id,
                    player.team_id,
                    player.jersey_number,
                    screen_x,
                    screen_y,
                    is_home
                )
                self.player_sprites[player.player_id] = sprite
            else:
                sprite = self.player_sprites[player.player_id]
                sprite.update_position(
                    screen_x, screen_y,
                    frame.timestamp,
                    player.x, player.y
                )
                
                # Update selection state
                if self.game_state.is_player_selected(player.player_id):
                    sprite.select()
                else:
                    sprite.deselect()
        
        # Remove sprites for players no longer in frame
        for player_id in existing_player_ids - current_player_ids:
            if player_id in self.player_sprites:
                del self.player_sprites[player_id]
        
        # Update ball
        if frame.ball:
            screen_x, screen_y = self.transformer.skillcorner_to_screen(
                frame.ball.x, frame.ball.y
            )
            
            if self.ball_sprite is None:
                self.ball_sprite = BallSprite(screen_x, screen_y)
            else:
                self.ball_sprite.update_position(screen_x, screen_y, frame.ball.z)
    
    def on_update(self, delta_time: float):
        """
        Update game state and sprites.
        
        Args:
            delta_time: Time elapsed since last update
        """
        # Update game state
        self.game_state.update(delta_time)
        
        # Update sprites based on current frame
        frame = self.game_state.get_current_frame()
        if frame:
            self._create_sprites_from_frame(frame)
        
        # Track FPS
        self.fps_history.append(1.0 / delta_time if delta_time > 0 else 60)
        if len(self.fps_history) > 60:
            self.fps_history.pop(0)
    
    def on_draw(self):
        """Render everything to the screen."""
        self.clear()
        
        # Draw pitch
        self.pitch_renderer.draw()
        
        # Draw sprites
        for sprite in self.player_sprites.values():
            sprite.draw()
        
        if self.ball_sprite:
            self.ball_sprite.draw()
        
        # Draw UI overlays
        self._draw_timeline()
        self._draw_telemetry_panel()
        self._draw_controls_help()
        self._draw_playback_info()
    
    def _draw_timeline(self):
        """Draw the timeline scrubber at the bottom."""
        if not self.game_state.show_timeline:
            return
        
        # Timeline background
        timeline_y = TIMELINE_MARGIN
        timeline_width = WINDOW_WIDTH - (2 * TIMELINE_MARGIN)
        
        arcade.draw_rectangle_filled(
            WINDOW_WIDTH / 2,
            timeline_y + TIMELINE_HEIGHT / 2,
            timeline_width,
            TIMELINE_HEIGHT,
            UI_BACKGROUND_COLOR
        )
        
        # Progress bar
        progress = self.game_state.get_progress_percentage() / 100.0
        arcade.draw_rectangle_filled(
            TIMELINE_MARGIN + (timeline_width * progress / 2),
            timeline_y + TIMELINE_HEIGHT / 2,
            timeline_width * progress,
            TIMELINE_HEIGHT - 10,
            arcade.color.RED
        )
        
        # Time labels
        current_time = self.game_state.format_time(
            self.game_state.get_current_timestamp()
        )
        total_time = self.game_state.format_time(
            self.game_state.get_total_duration()
        )
        
        arcade.draw_text(
            f"{current_time} / {total_time}",
            WINDOW_WIDTH / 2,
            timeline_y + TIMELINE_HEIGHT / 2,
            UI_TEXT_COLOR,
            font_size=UI_FONT_SIZE,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
    
    def _draw_telemetry_panel(self):
        """Draw player telemetry panel on the right side."""
        if not self.game_state.show_telemetry:
            return
        
        if self.game_state.selected_player_id is None:
            return
        
        # Panel background
        panel_x = WINDOW_WIDTH - TELEMETRY_PANEL_WIDTH / 2
        panel_y = WINDOW_HEIGHT / 2
        
        arcade.draw_rectangle_filled(
            panel_x,
            panel_y,
            TELEMETRY_PANEL_WIDTH,
            WINDOW_HEIGHT - 200,
            UI_BACKGROUND_COLOR
        )
        
        # Get selected player metrics
        sprite = self.player_sprites.get(self.game_state.selected_player_id)
        if not sprite:
            return
        
        metrics = sprite.get_metrics_dict()
        player_info = self.game_state.get_player_info(sprite.player_id)
        
        # Draw player info
        text_x = WINDOW_WIDTH - TELEMETRY_PANEL_WIDTH + TELEMETRY_PANEL_PADDING
        text_y = WINDOW_HEIGHT - 150
        line_height = 25
        
        lines = [
            f"PLAYER: {player_info.get('name', 'Unknown')}",
            f"#{metrics['jersey_number']} - {player_info.get('position', 'N/A')}",
            f"Team: {player_info.get('team_name', 'Unknown')}",
            "",
            "CURRENT METRICS",
            f"Speed: {metrics['current_speed_kmh']:.1f} km/h",
            f"Distance: {metrics['total_distance_m']:.0f} m",
            f"Sprint Dist: {metrics['sprint_distance_m']:.0f} m",
            f"Sprint %: {metrics['sprint_percentage']:.1f}%",
        ]
        
        for i, line in enumerate(lines):
            arcade.draw_text(
                line,
                text_x,
                text_y - (i * line_height),
                UI_TEXT_COLOR,
                font_size=UI_FONT_SIZE if i > 3 else UI_FONT_SIZE + 2,
                bold=(i == 0 or i == 4)
            )
    
    def _draw_controls_help(self):
        """Draw control hints in top-left corner."""
        help_text = [
            "CONTROLS:",
            "SPACE - Pause/Play",
            "1-4 - Playback Speed",
            "R - Restart",
            "← → - Skip 5s",
            "T - Toggle Timeline",
            "Click Player - Select"
        ]
        
        x = 20
        y = WINDOW_HEIGHT - 40
        
        for i, line in enumerate(help_text):
            arcade.draw_text(
                line,
                x,
                y - (i * 20),
                UI_TEXT_COLOR,
                font_size=12,
                bold=(i == 0)
            )
    
    def _draw_playback_info(self):
        """Draw playback status in top-right corner."""
        info_lines = [
            f"{'PAUSED' if self.game_state.is_paused else 'PLAYING'}",
            f"Speed: {self.game_state.playback_speed}x",
            f"Frame: {self.game_state.current_frame_index}/{self.game_state.get_total_frames()}",
        ]
        
        # Add FPS if available
        if self.fps_history:
            avg_fps = sum(self.fps_history) / len(self.fps_history)
            info_lines.append(f"FPS: {avg_fps:.0f}")
        
        x = WINDOW_WIDTH - 200
        y = WINDOW_HEIGHT - 40
        
        for i, line in enumerate(info_lines):
            arcade.draw_text(
                line,
                x,
                y - (i * 20),
                UI_TEXT_COLOR,
                font_size=12,
                bold=(i == 0)
            )
    
    def on_key_press(self, key, modifiers):
        """
        Handle keyboard input.
        
        Args:
            key: Key code
            modifiers: Modifier keys held
        """
        # Playback controls
        if key == arcade.key.SPACE:
            self.game_state.toggle_pause()
        
        elif key == arcade.key.KEY_1:
            self.game_state.set_playback_speed(0.25)
        elif key == arcade.key.KEY_2:
            self.game_state.set_playback_speed(0.5)
        elif key == arcade.key.KEY_3:
            self.game_state.set_playback_speed(1.0)
        elif key == arcade.key.KEY_4:
            self.game_state.set_playback_speed(2.0)
        elif key == arcade.key.KEY_5:
            self.game_state.set_playback_speed(4.0)
        
        elif key == arcade.key.R:
            self.game_state.restart()
        
        # Navigation
        elif key == arcade.key.LEFT:
            frames_to_skip = int(FRAME_SKIP_SECONDS * DATA_FPS)
            self.game_state.rewind_frames(frames_to_skip)
        
        elif key == arcade.key.RIGHT:
            frames_to_skip = int(FRAME_SKIP_SECONDS * DATA_FPS)
            self.game_state.advance_frames(frames_to_skip)
        
        # UI toggles
        elif key == arcade.key.T:
            self.game_state.show_timeline = not self.game_state.show_timeline
        
        elif key == arcade.key.H:
            self.game_state.toggle_overlay('heatmap')
        
        elif key == arcade.key.P:
            self.game_state.toggle_overlay('pass_network')
        
        elif key == arcade.key.F:
            self.game_state.toggle_overlay('formation')
    
    def on_mouse_motion(self, x, y, dx, dy):
        """Track mouse position."""
        self.mouse_x = x
        self.mouse_y = y
    
    def on_mouse_press(self, x, y, button, modifiers):
        """
        Handle mouse clicks.
        
        Args:
            x, y: Click position
            button: Mouse button
            modifiers: Modifier keys held
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Check if clicking on a player
            clicked_player = self._get_player_at_position(x, y)
            if clicked_player:
                if self.game_state.is_player_selected(clicked_player.player_id):
                    self.game_state.deselect_player()
                else:
                    self.game_state.select_player(clicked_player.player_id)
    
    def _get_player_at_position(self, x: float, y: float) -> Optional[PlayerSprite]:
        """
        Find player sprite at given screen position.
        
        Args:
            x, y: Screen coordinates
            
        Returns:
            PlayerSprite if found, None otherwise
        """
        for sprite in self.player_sprites.values():
            distance = ((sprite.center_x - x) ** 2 + 
                       (sprite.center_y - y) ** 2) ** 0.5
            if distance <= sprite.radius * 2:  # Click tolerance
                return sprite
        return None