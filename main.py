import pygame
import sys
import random

from hand_tracker import HandTracker
from game_objects import Fruit, Bomb
from mechanics import ScoreSystem, GameEngine
from visuals import ParticleSystem, SwordTrail
from ui import UI

def main():
    pygame.init()
    
    # Constants
    WIDTH, HEIGHT = 800, 600
    FPS = 60
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AI Fruit Ninja - Project Expo")
    clock = pygame.time.Clock()
    
    # Try to load background
    try:
        background = pygame.image.load("assets/background.jpg").convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    except:
        background = pygame.Surface((WIDTH, HEIGHT))
        background.fill((20, 20, 40))

    # Initialize Modules
    tracker = HandTracker(camera_index=0, smoothing_factor=0.4)
    ui = UI(WIDTH, HEIGHT)
    score_sys = ScoreSystem()
    particles = ParticleSystem()
    sword = SwordTrail(max_length=12)

    # Game State
    active_objects = []
    state = "START"  # START, PLAY, GAMEOVER
    spawn_timer = 0
    
    running = True
    
    def spawn_object():
        # 15% chance for bomb, otherwise fruit
        if random.random() < 0.15:
            active_objects.append(Bomb(WIDTH, HEIGHT))
        else:
            active_objects.append(Fruit(WIDTH, HEIGHT))

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Allow mouse control as fallback
            if event.type == pygame.MOUSEMOTION and not tracker.is_detected:
                sword.add_point(event.pos)

        # Update MediaPipe Tracking
        hand_pos = tracker.get_position(WIDTH, HEIGHT)
        if hand_pos:
            sword.add_point(hand_pos)
            
            # Simple state transitions using hand presence
            # e.g., Raise hand to start
            if state in ["START", "GAMEOVER"]:
                state = "PLAY"
                active_objects.clear()
                score_sys.reset()
        else:
            sword.add_point(None)
            
        # Draw background
        screen.blit(background, (0, 0))

        if state == "PLAY":
            # Spawning
            spawn_timer += 1
            if spawn_timer > max(40, 100 - score_sys.score):  # Gets faster
                spawn_object()
                spawn_timer = 0

            # Update and Draw Objects
            for obj in active_objects[:]:
                obj.update()
                
                # Check bounds
                if obj.y > HEIGHT + 100:
                    if obj in active_objects:
                        active_objects.remove(obj)
                        if isinstance(obj, Fruit):
                            score_sys.combo_count = 0  # Missed a fruit breaks combo
                    continue
                
                obj.draw(screen)
                
                # Check collision if we have a sword segment
                segment = sword.get_slice_segment()
                if segment and not obj.is_sliced:
                    p1, p2 = segment
                    # Adjust collision radius slightly smaller for better precision
                    if GameEngine.check_collision(p1, p2, obj.get_center(), obj.radius * 0.8):
                        obj.is_sliced = True
                        
                        if isinstance(obj, Bomb):
                            # Boom
                            particles.spawn(obj.x, obj.y, (255,100,0), count=50)
                            state = "GAMEOVER"
                        else:
                            # Sliced
                            particles.spawn(obj.x, obj.y, obj.color, count=20)
                            score_sys.add_score(obj.points)
                        
                        if obj in active_objects:
                            active_objects.remove(obj)

            # Updates Particles
            particles.update()
            
            # Draw HUD
            ui.draw_hud(screen, score_sys.score, score_sys.high_score, score_sys.combo_count)

        # Draw Particles and Sword (always drawn)
        for p in particles.particles:
            # Reusing the particle logic from visuals.py but need to actually draw it here if we want to layer properly
            # Or just call particles.draw
            pass
        particles.draw(screen)
        sword.draw(screen)

        # Draw Menus
        if state == "START":
            ui.draw_start_screen(screen)
        elif state == "GAMEOVER":
            ui.draw_game_over(screen, score_sys.score)
            
        # Draw Expo Mode
        ui.draw_expo_mode(screen, tracker.get_expo_stats(), clock.get_fps())

        pygame.display.flip()
        clock.tick(FPS)

    # Cleanup
    tracker.stop()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
