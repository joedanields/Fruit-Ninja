import pygame
import sys
import random

from hand_tracker import HandTracker
from game_objects import Fruit, Bomb
from mechanics import ScoreSystem, GameEngine, DifficultyManager
from visuals import ParticleSystem, SwordTrail, ScreenShake
from ui import UI

# Constants for better organization and performance
class GameConstants:
    WIDTH = 800
    HEIGHT = 600
    FPS = 60
    BASE_SPAWN_DELAY = 100
    MIN_SPAWN_DELAY = 30
    SPAWN_SPEED_INCREASE = 0.5  # How much faster spawning gets per point
    COLLISION_RADIUS_FACTOR = 0.8  # Collision precision factor
    MAX_OBJECTS = 30  # Prevent memory issues with too many objects

def main():
    pygame.init()
    
    screen = pygame.display.set_mode((GameConstants.WIDTH, GameConstants.HEIGHT))
    pygame.display.set_caption("AI Fruit Ninja - Project Expo")
    clock = pygame.time.Clock()
    
    # Try to load background
    try:
        background = pygame.image.load("assets/background.jpg").convert()
        background = pygame.transform.scale(background, (GameConstants.WIDTH, GameConstants.HEIGHT))
    except:
        background = pygame.Surface((GameConstants.WIDTH, GameConstants.HEIGHT))
        background.fill((20, 20, 40))

    # Initialize Modules
    tracker = HandTracker(camera_index=0, smoothing_factor=0.4)
    ui = UI(GameConstants.WIDTH, GameConstants.HEIGHT)
    score_sys = ScoreSystem()
    particles = ParticleSystem()
    sword = SwordTrail(max_length=12)
    screen_shake = ScreenShake()

    # Game State
    active_objects = []
    state = "START"  # START, PLAY, GAMEOVER
    spawn_timer = 0
    
    running = True
    
    def spawn_object():
        """Spawn a new fruit or bomb with dynamic difficulty"""
        if len(active_objects) >= GameConstants.MAX_OBJECTS:
            return  # Prevent spawning too many objects
        
        # Get dynamic bomb chance based on score
        bomb_chance = DifficultyManager.get_bomb_chance(score_sys.score)
        
        if random.random() < bomb_chance:
            active_objects.append(Bomb(GameConstants.WIDTH, GameConstants.HEIGHT))
        else:
            active_objects.append(Fruit(GameConstants.WIDTH, GameConstants.HEIGHT))
    
    def calculate_spawn_delay():
        """Calculate dynamic spawn delay based on score and difficulty"""
        speed_mult = DifficultyManager.get_speed_multiplier(score_sys.score)
        delay = max(
            GameConstants.MIN_SPAWN_DELAY,
            GameConstants.BASE_SPAWN_DELAY - score_sys.score * GameConstants.SPAWN_SPEED_INCREASE
        )
        # Apply difficulty speed multiplier
        delay = delay / speed_mult
        return int(delay)

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Allow mouse control as fallback
            elif event.type == pygame.MOUSEMOTION and not tracker.is_detected:
                sword.add_point(event.pos)

        # Update MediaPipe Tracking
        hand_pos = tracker.get_position(GameConstants.WIDTH, GameConstants.HEIGHT)
        if hand_pos:
            sword.add_point(hand_pos)
            
            # Simple state transitions using hand presence
            if state in ["START", "GAMEOVER"]:
                state = "PLAY"
                active_objects.clear()
                score_sys.reset()
        else:
            sword.add_point(None)
        
        # Update screen shake
        screen_shake.update()
            
        # Draw background with shake effect
        screen_shake.apply_to_screen(screen, background)

        if state == "PLAY":
            # Dynamic spawning with difficulty progression
            spawn_timer += 1
            spawn_delay = calculate_spawn_delay()
            
            if spawn_timer > spawn_delay:
                spawn_object()
                spawn_timer = 0

            # Get slice segment once for all collision checks
            slice_segment = sword.get_slice_segment()
            
            # Update and Draw Objects (optimized with list comprehension)
            objects_to_remove = []
            
            for obj in active_objects:
                obj.update()
                
                # Check bounds - mark for removal if off screen
                if obj.y > GameConstants.HEIGHT + 100:
                    if isinstance(obj, Fruit):
                        score_sys.combo_count = 0  # Missed a fruit breaks combo
                    objects_to_remove.append(obj)
                    continue
                
                obj.draw(screen)
                
                # Check collision with optimized conditions
                if slice_segment and not obj.is_sliced and obj.is_active:
                    p1, p2 = slice_segment
                    # Use cached center position and adjusted collision radius
                    if GameEngine.check_collision(
                        p1, p2, 
                        obj.get_center(), 
                        obj.radius * GameConstants.COLLISION_RADIUS_FACTOR
                    ):
                        obj.is_sliced = True
                        
                        if isinstance(obj, Bomb):
                            # Bomb explosion with screen shake
                            particles.spawn(obj.center_x, obj.center_y, (255, 100, 0), count=50)
                            screen_shake.trigger(intensity=15, duration=15)
                            state = "GAMEOVER"
                        else:
                            # Fruit sliced
                            particles.spawn(obj.center_x, obj.center_y, obj.color, count=20)
                            score_sys.add_score(obj.points)
                        
                        objects_to_remove.append(obj)
            
            # Batch removal for better performance
            for obj in objects_to_remove:
                if obj in active_objects:
                    active_objects.remove(obj)

            # Update Particles
            particles.update()
            
            # Get current difficulty for display
            current_difficulty = DifficultyManager.get_difficulty(score_sys.score)
            
            # Draw HUD
            ui.draw_hud(screen, score_sys.score, score_sys.high_score, 
                       score_sys.combo_count, current_difficulty)

        # Draw Particles and Sword (always drawn)
        particles.draw(screen)
        sword.draw(screen)

        # Draw Menus
        if state == "START":
            ui.draw_start_screen(screen)
        elif state == "GAMEOVER":
            ui.draw_game_over(screen, score_sys.score)
            
        # Draw Expo Mode telemetry
        ui.draw_expo_mode(screen, tracker.get_expo_stats(), clock.get_fps())

        pygame.display.flip()
        clock.tick(GameConstants.FPS)

    # Cleanup
    tracker.stop()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
