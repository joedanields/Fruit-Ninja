import pygame
import random

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def spawn(self, x, y, color, count=15):
        for _ in range(count):
            particle = {
                'x': x,
                'y': y,
                'vx': random.uniform(-5, 5),
                'vy': random.uniform(-10, 5),
                'life': random.randint(20, 40),
                'color': color,
                'size': random.randint(3, 8)
            }
            self.particles.append(particle)

    def update(self):
        for p in self.particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.5  # gravity
            p['life'] -= 1
            if p['life'] <= 0:
                self.particles.remove(p)

    def draw(self, screen):
        for p in self.particles:
            alpha = max(0, int((p['life'] / 40) * 255))
            color_with_alpha = (*p['color'], alpha)
            
            # Draw particle on a temp surface for alpha support
            surface = pygame.Surface((p['size']*2, p['size']*2), pygame.SRCALPHA)
            pygame.draw.circle(surface, color_with_alpha, (p['size'], p['size']), p['size'])
            screen.blit(surface, (int(p['x'] - p['size']), int(p['y'] - p['size'])))


class SwordTrail:
    def __init__(self, max_length=15):
        self.points = []
        self.max_length = max_length
        self.color_core = (255, 255, 255)
        self.color_glow = (0, 255, 255)

    def add_point(self, pos):
        if pos:
            self.points.append(pos)
            if len(self.points) > self.max_length:
                self.points.pop(0)
        else:
            # If tracking lost, slowly reduce trail
            if self.points:
                self.points.pop(0)

    def draw(self, screen):
        if len(self.points) < 2:
            return

        # Draw glowing trail
        for i in range(1, len(self.points)):
            p1 = self.points[i-1]
            p2 = self.points[i]
            
            # Increase thickness towards the tip
            thickness = int((i / len(self.points)) * 12)
            
            if thickness > 0:
                # Glow
                pygame.draw.line(screen, self.color_glow, p1, p2, thickness + 6)
                # Core
                pygame.draw.line(screen, self.color_core, p1, p2, thickness)
                
                # Connecting circles for smooth joints
                pygame.draw.circle(screen, self.color_core, (int(p2[0]), int(p2[1])), thickness // 2)

    def get_slice_segment(self):
        """Returns the last two points to check for collision."""
        if len(self.points) >= 2:
            return self.points[-2], self.points[-1]
        return None
