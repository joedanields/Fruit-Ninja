import pygame
import random
import math

class GameObject:
    # Rotation cache for performance (shared across all instances)
    _rotation_cache = {}
    _cache_limit = 200  # Limit cache size
    
    def __init__(self, x, y, image_path, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.image_path = image_path
        
        try:
            self.original_image = pygame.image.load(image_path).convert_alpha()
        except Exception:
            # Fallback if image not found
            self.original_image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(self.original_image, (255, 0, 0), (radius, radius), radius)
        
        self.image = self.original_image
        self.width = self.original_image.get_width()
        self.height = self.original_image.get_height()
        
        # Physics
        self.velocity_x = random.uniform(-3, 3)
        self.velocity_y = random.uniform(-14, -18)
        self.gravity = 0.4
        
        # Rotation
        self.angle = 0
        self.rotation_speed = random.uniform(-5, 5)
        self.last_rendered_angle = None
        
        # Pre-calculate center offset
        self.center_x = self.x + self.width // 2
        self.center_y = self.y + self.height // 2
        self.rect = self.image.get_rect(center=(self.center_x, self.center_y))
        
        self.is_sliced = False
        self.is_active = True

    def _get_rotated_image(self, angle):
        """Get cached rotated image or create new one"""
        # Round angle to nearest 5 degrees for caching
        cache_angle = round(angle / 5) * 5
        cache_key = (self.image_path, cache_angle)
        
        if cache_key not in GameObject._rotation_cache:
            # Clean cache if too large
            if len(GameObject._rotation_cache) > GameObject._cache_limit:
                GameObject._rotation_cache.clear()
            
            GameObject._rotation_cache[cache_key] = pygame.transform.rotate(
                self.original_image, cache_angle
            )
        
        return GameObject._rotation_cache[cache_key]

    def update(self):
        if not self.is_sliced and self.is_active:
            # Apply physics
            self.velocity_y += self.gravity
            self.x += self.velocity_x
            self.y += self.velocity_y
            
            # Update center position
            self.center_x = self.x + self.width // 2
            self.center_y = self.y + self.height // 2
            
            # Apply rotation (cached)
            self.angle = (self.angle + self.rotation_speed) % 360
            
            # Only update image if angle changed significantly
            if self.last_rendered_angle is None or abs(self.angle - self.last_rendered_angle) >= 5:
                self.image = self._get_rotated_image(self.angle)
                self.last_rendered_angle = round(self.angle / 5) * 5
            
            # Update rect for new position
            self.rect = self.image.get_rect(center=(self.center_x, self.center_y))

    def draw(self, screen):
        if not self.is_sliced and self.is_active:
            screen.blit(self.image, self.rect)

    def get_center(self):
        """Return cached center position for performance"""
        return (self.center_x, self.center_y)
    
    def deactivate(self):
        """Mark object as inactive for removal"""
        self.is_active = False


class Fruit(GameObject):
    # Pre-define types as class variable for better memory usage
    TYPES = {
        'watermelon': {'points': 10, 'image': 'assets/watermelon.png', 'color': (220, 20, 40)},
        'apple': {'points': 5, 'image': 'assets/apple.png', 'color': (220, 20, 20)},
        'orange': {'points': 7, 'image': 'assets/orange.png', 'color': (255, 140, 0)},
        'banana': {'points': 15, 'image': 'assets/banana.png', 'color': (255, 225, 0)}
    }
    
    # Cache fruit type keys to avoid repeated list() calls
    _type_keys = list(TYPES.keys())

    def __init__(self, screen_width, screen_height):
        fruit_type = random.choice(Fruit._type_keys)
        data = Fruit.TYPES[fruit_type]
        
        self.fruit_type = fruit_type
        self.points = data['points']
        self.color = data['color']
        
        x_pos = random.randint(100, screen_width - 100)
        y_pos = screen_height + 50
        radius = 40
        super().__init__(x_pos, y_pos, data['image'], radius)


class Bomb(GameObject):
    def __init__(self, screen_width, screen_height):
        self.points = 0
        self.color = (255, 100, 0)
        x_pos = random.randint(100, screen_width - 100)
        y_pos = screen_height + 50
        radius = 35
        super().__init__(x_pos, y_pos, 'assets/bomb.png', radius)
