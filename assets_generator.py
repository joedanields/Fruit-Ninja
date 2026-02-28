import os
import pygame
import math

# Initialize pygame surface explicitly without display
pygame.init()

ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

def create_image(name, size, draw_func):
    surface = pygame.Surface(size, pygame.SRCALPHA)
    draw_func(surface)
    pygame.image.save(surface, os.path.join(ASSETS_DIR, name))

def draw_apple(surface):
    # Red apple body
    pygame.draw.circle(surface, (220, 20, 20), (50, 55), 40)
    # Stem
    pygame.draw.rect(surface, (100, 50, 20), (45, 10, 10, 15))
    # Leaf
    pygame.draw.ellipse(surface, (34, 139, 34), (55, 15, 20, 10))

def draw_orange(surface):
    # Orange body
    pygame.draw.circle(surface, (255, 140, 0), (50, 50), 40)
    # Texture / Highlight
    pygame.draw.circle(surface, (255, 165, 0), (35, 35), 10)
    # Stem dot
    pygame.draw.circle(surface, (34, 139, 34), (50, 10), 3)

def draw_watermelon(surface):
    # Green rind
    pygame.draw.circle(surface, (0, 100, 0), (50, 50), 45)
    # Light green inner rind
    pygame.draw.circle(surface, (144, 238, 144), (50, 50), 38)
    # Red flesh
    pygame.draw.circle(surface, (220, 20, 40), (50, 50), 32)
    # Stripes
    for i in range(0, 360, 45):
        rad = math.radians(i)
        x = int(50 + 45 * math.cos(rad))
        y = int(50 + 45 * math.sin(rad))
        pygame.draw.line(surface, (0, 150, 0), (50, 50), (x, y), 2)

def draw_banana(surface):
    # Yellow banana curve
    rect = pygame.Rect(20, 20, 60, 60)
    pygame.draw.arc(surface, (255, 225, 0), rect, math.radians(180), math.radians(360), 15)
    # Tips
    pygame.draw.circle(surface, (139, 69, 19), (20, 50), 7)
    pygame.draw.circle(surface, (139, 69, 19), (80, 50), 7)

def draw_bomb(surface):
    # Black body
    pygame.draw.circle(surface, (30, 30, 30), (50, 60), 35)
    # Cap
    pygame.draw.rect(surface, (100, 100, 100), (40, 20, 20, 10))
    # Spark sparkler
    pygame.draw.line(surface, (150, 100, 50), (50, 20), (60, 5), 3)
    # Spark
    pygame.draw.circle(surface, (255, 69, 0), (60, 5), 5)
    pygame.draw.circle(surface, (255, 215, 0), (60, 5), 3)

def draw_background(surface):
    # Simple radial gradient for background
    for radius in range(800, 0, -5):
        color_val = max(20, min(100, int(radius / 800 * 80) + 20))
        color = (10, color_val, int(color_val * 1.5))
        pygame.draw.circle(surface, color, (400, 300), radius)
    # Grid pattern
    for x in range(0, 800, 40):
        pygame.draw.line(surface, (30, 50, 70), (x, 0), (x, 600), 1)
    for y in range(0, 600, 40):
        pygame.draw.line(surface, (30, 50, 70), (0, y), (800, y), 1)

def main():
    print("Generating assets...")
    create_image("apple.png", (100, 100), draw_apple)
    create_image("orange.png", (100, 100), draw_orange)
    create_image("watermelon.png", (100, 100), draw_watermelon)
    create_image("banana.png", (100, 100), draw_banana)
    create_image("bomb.png", (100, 100), draw_bomb)

    # Note: background should be a full screen size usually (e.g. 800x600 for pygame standard)
    create_image("background.jpg", (800, 600), draw_background)
    print("Assets generated in 'assets' directory.")

if __name__ == "__main__":
    main()
