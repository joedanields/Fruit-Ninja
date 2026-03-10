"""
Main game loop for AI Fruit Ninja
Handles game initialization, state management, and rendering
"""
import pygame
import sys
import random
from pathlib import Path
from typing import Optional

# Import from package modules
from .hand_tracker import HandTracker
from .game_objects import Fruit, Bomb
from .mechanics import ScoreSystem, GameEngine, DifficultyManager, Leaderboard
from .visuals import ParticleSystem, SwordTrail, ScreenShake
from .ui import UI

# For asset loading when installed as package
try:
    from importlib.resources import files, as_file
except ImportError:
    # Fallback for Python < 3.9
    from importlib_resources import files, as_file


# Constants for better organization and performance
class GameConstants:
    """Game configuration constants"""
    WIDTH = 800
    HEIGHT = 600
    FPS = 60
    BASE_SPAWN_DELAY = 100
    MIN_SPAWN_DELAY = 30
    SPAWN_SPEED_INCREASE = 0.5
    COLLISION_RADIUS_FACTOR = 0.8
    MAX_OBJECTS = 30


def get_asset_path(filename: str) -> Optional[Path]:
    """
    Get the path to an asset file, handling both development and installed package scenarios.
    
    Args:
        filename: Name of the asset file (e.g., 'background.jpg')
    
    Returns:
        Path object to the asset file, or None if not found
    """
    try:
        # Try to load from package resources (when installed)
        asset_files = files('ai_fruit_ninja').joinpath('assets')
        return Path(asset_files) / filename
    except (TypeError, FileNotFoundError, AttributeError):
        # Fallback to local assets folder (development mode)
        local_assets = Path(__file__).parent / 'assets' / filename
        if local_assets.exists():
            return local_assets
        # Try parent directory (for backward compatibility)
        parent_assets = Path(__file__).parent.parent / 'assets' / filename
        if parent_assets.exists():
            return parent_assets
    return None


def load_background(width: int, height: int) -> pygame.Surface:
    """
    Load and scale the background image.
    
    Args:
        width: Target width for scaling
        height: Target height for scaling
    
    Returns:
        Pygame Surface with background
    """
    background_path = get_asset_path('background.jpg')
    
    if background_path and background_path.exists():
        try:
            background = pygame.image.load(str(background_path)).convert()
            return pygame.transform.scale(background, (width, height))
        except pygame.error:
            pass
    
    # Fallback: create a solid color background
    background = pygame.Surface((width, height))
    background.fill((20, 20, 40))
    return background


def run_game() -> None:
    """
    Main entry point for the AI Fruit Ninja game.
    
    This function initializes the game, handles the main game loop,
    and manages cleanup on exit.
    """
    pygame.init()
    
    # Setup display
    screen = pygame.display.set_mode((GameConstants.WIDTH, GameConstants.HEIGHT))
    pygame.display.set_caption("AI Fruit Ninja - Hand Tracking Edition")
    clock = pygame.time.Clock()
    
    # Load background
    background = load_background(GameConstants.WIDTH, GameConstants.HEIGHT)

    # Initialize game modules
    tracker = HandTracker(camera_index=0, smoothing_factor=0.4)
    ui = UI(GameConstants.WIDTH, GameConstants.HEIGHT)
    score_sys = ScoreSystem()
    particles = ParticleSystem()
    sword = SwordTrail(max_length=12)
    screen_shake = ScreenShake()
    leaderboard = Leaderboard()

    # Game state
    active_objects = []
    state = "NAME_INPUT"  # NAME_INPUT, WAITING_HAND, PLAY, GAMEOVER, LEADERBOARD
    spawn_timer = 0
    running = True
    player_name = ""
    current_rank = None
    is_high_score = False
    
    def spawn_object() -> None:
        """Spawn a new fruit or bomb with dynamic difficulty"""
        if len(active_objects) >= GameConstants.MAX_OBJECTS:
            return
        
        bomb_chance = DifficultyManager.get_bomb_chance(score_sys.score)
        
        if random.random() < bomb_chance:
            active_objects.append(Bomb(GameConstants.WIDTH, GameConstants.HEIGHT))
        else:
            active_objects.append(Fruit(GameConstants.WIDTH, GameConstants.HEIGHT))
    
    def calculate_spawn_delay() -> int:
        """Calculate dynamic spawn delay based on score and difficulty"""
        speed_mult = DifficultyManager.get_speed_multiplier(score_sys.score)
        delay = max(
            GameConstants.MIN_SPAWN_DELAY,
            GameConstants.BASE_SPAWN_DELAY - score_sys.score * GameConstants.SPAWN_SPEED_INCREASE
        )
        delay = delay / speed_mult
        return int(delay)

    # Main game loop
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION and not tracker.is_detected:
                sword.add_point(event.pos)
            
            # Handle keyboard input
            elif event.type == pygame.KEYDOWN:
                if state == "NAME_INPUT":
                    if event.key == pygame.K_RETURN and player_name.strip():
                        # Submit name and move to hand detection
                        state = "WAITING_HAND"
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.unicode.isprintable() and len(player_name) < 20:
                        player_name += event.unicode
                
                elif state == "LEADERBOARD":
                    if event.key == pygame.K_SPACE:
                        # Restart game
                        state = "NAME_INPUT"
                        player_name = ""
                        active_objects.clear()
                        score_sys.reset()
                        current_rank = None
                        is_high_score = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False

        # Update hand tracking
        hand_pos = tracker.get_position(GameConstants.WIDTH, GameConstants.HEIGHT)
        if hand_pos:
            sword.add_point(hand_pos)
            
            # Transition from waiting to playing when hand detected
            if state == "WAITING_HAND":
                state = "PLAY"
                active_objects.clear()
                score_sys.reset()
        else:
            sword.add_point(None)
        
        # Update visual effects
        screen_shake.update()
        screen_shake.apply_to_screen(screen, background)

        # Gameplay logic
        if state == "PLAY":
            spawn_timer += 1
            spawn_delay = calculate_spawn_delay()
            
            if spawn_timer > spawn_delay:
                spawn_object()
                spawn_timer = 0

            slice_segment = sword.get_slice_segment()
            objects_to_remove = []
            
            for obj in active_objects:
                obj.update()
                
                if obj.y > GameConstants.HEIGHT + 100:
                    if isinstance(obj, Fruit):
                        score_sys.combo_count = 0
                    objects_to_remove.append(obj)
                    continue
                
                obj.draw(screen)
                
                if slice_segment and not obj.is_sliced and obj.is_active:
                    p1, p2 = slice_segment
                    if GameEngine.check_collision(
                        p1, p2, 
                        obj.get_center(), 
                        obj.radius * GameConstants.COLLISION_RADIUS_FACTOR
                    ):
                        obj.is_sliced = True
                        
                        if isinstance(obj, Bomb):
                            particles.spawn(obj.center_x, obj.center_y, (255, 100, 0), count=50)
                            screen_shake.trigger(intensity=15, duration=15)
                            # Add score to leaderboard
                            is_high_score, current_rank = leaderboard.add_score(
                                player_name, score_sys.score
                            )
                            state = "GAMEOVER"
                        else:
                            particles.spawn(obj.center_x, obj.center_y, obj.color, count=20)
                            score_sys.add_score(obj.points)
                        
                        objects_to_remove.append(obj)
            
            for obj in objects_to_remove:
                if obj in active_objects:
                    active_objects.remove(obj)

            particles.update()
            current_difficulty = DifficultyManager.get_difficulty(score_sys.score)
            ui.draw_hud(screen, score_sys.score, score_sys.high_score, 
                       score_sys.combo_count, current_difficulty)

        # Render
        particles.draw(screen)
        sword.draw(screen)

        if state == "NAME_INPUT":
            ui.draw_name_input_screen(screen, player_name)
        elif state == "WAITING_HAND":
            ui.draw_waiting_for_hand(screen)
        elif state == "GAMEOVER":
            ui.draw_game_over(screen, score_sys.score)
            # Automatically transition to leaderboard after a brief delay
            pygame.time.wait(2000)
            state = "LEADERBOARD"
        elif state == "LEADERBOARD":
            ui.draw_leaderboard(
                screen, 
                leaderboard, 
                player_name, 
                score_sys.score,
                is_high_score
            )
            
        ui.draw_expo_mode(screen, tracker.get_expo_stats(), clock.get_fps())

        pygame.display.flip()
        clock.tick(GameConstants.FPS)

    # Cleanup
    tracker.stop()
    pygame.quit()
    sys.exit(0)


def main() -> None:
    """Alias for run_game() for backward compatibility"""
    run_game()


if __name__ == "__main__":
    run_game()
