import pygame
import random
import math

class GameObject:
    def __init__(self, x, y, image_path, radius):
        self.x = x
        self.y = y
        self.radius = radius
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except Exception:
            # Fallback if image not found
            self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 0, 0), (radius, radius), radius)
            
        self.original_image = self.image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        # Physics
        self.velocity_x = random.uniform(-3, 3)
        self.velocity_y = random.uniform(-14, -18)
        self.gravity = 0.4
        
        # Rotation
        self.angle = 0
        self.rotation_speed = random.uniform(-5, 5)
        
        self.is_sliced = False

    def update(self):
        if not self.is_sliced:
            # Apply physics
            self.velocity_y += self.gravity
            self.x += self.velocity_x
            self.y += self.velocity_y
            
            # Apply rotation
            self.angle = (self.angle + self.rotation_speed) % 360
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            
            # Re-center image after rotation
            self.rect = self.image.get_rect(center=(self.x + self.width//2, self.y + self.height//2))

    def draw(self, screen):
        if not self.is_sliced:
            screen.blit(self.image, self.rect)

    def get_center(self):
        return (self.rect.centerx, self.rect.centery)


class Fruit(GameObject):
    TYPES = {
        'watermelon': {'points': 10, 'image': 'assets/watermelon.png', 'color': (220, 20, 40)},
        'apple': {'points': 5, 'image': 'assets/apple.png', 'color': (220, 20, 20)},
        'orange': {'points': 7, 'image': 'assets/orange.png', 'color': (255, 140, 0)},
        'banana': {'points': 15, 'image': 'assets/banana.png', 'color': (255, 225, 0)}
    }

    def __init__(self, screen_width, screen_height):
        fruit_type = random.choice(list(self.TYPES.keys()))
        data = self.TYPES[fruit_type]
        self.points = data['points']
        self.color = data['color']
        
        x_pos = random.randint(100, screen_width - 100)
        y_pos = screen_height + 50
        radius = 40
        super().__init__(x_pos, y_pos, data['image'], radius)


class Bomb(GameObject):
    def __init__(self, screen_width, screen_height):
        self.points = 0
        x_pos = random.randint(100, screen_width - 100)
        y_pos = screen_height + 50
        radius = 35
        super().__init__(x_pos, y_pos, 'assets/bomb.png', radius)
