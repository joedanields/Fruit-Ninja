import pygame
import random
import math

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def spawn(self, x, y, color, count=15):
        """Spawn particles with enhanced variety"""
        for _ in range(count):
            particle = {
                'x': x,
                'y': y,
                'vx': random.uniform(-6, 6),
                'vy': random.uniform(-12, 3),
                'life': random.randint(20, 50),
                'max_life': random.randint(20, 50),
                'color': color,
                'size': random.randint(3, 9),
                'gravity': random.uniform(0.3, 0.6)
            }
            self.particles.append(particle)

    def update(self):
        """Update particles with optimized removal"""
        # Use list comprehension for better performance
        alive_particles = []
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += p['gravity']  # Individual gravity
            p['life'] -= 1
            
            # Apply air resistance for more realistic motion
            p['vx'] *= 0.98
            
            if p['life'] > 0:
                alive_particles.append(p)
        
        self.particles = alive_particles

    def draw(self, screen):
        """Draw particles with fade-out effect"""
        for p in self.particles:
            # Calculate alpha based on remaining life
            life_ratio = p['life'] / p['max_life']
            alpha = max(0, min(255, int(life_ratio * 255)))
            
            # Shrink particle over time
            current_size = max(1, int(p['size'] * life_ratio))
            
            # Ensure color is RGB tuple (not RGBA)
            color = p['color']
            if len(color) > 3:
                color = color[:3]
            color_with_alpha = (color[0], color[1], color[2], alpha)
            
            # Draw particle on a temp surface for alpha support
            surface = pygame.Surface((current_size * 2, current_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, color_with_alpha, (current_size, current_size), current_size)
            screen.blit(surface, (int(p['x'] - current_size), int(p['y'] - current_size)))


class SwordTrail:
    def __init__(self, max_length=15):
        self.points = []
        self.max_length = max_length
        self.color_core = (255, 255, 255)
        self.color_glow = (0, 255, 255)
        self.velocity = []  # Track velocity for motion effect

    def add_point(self, pos):
        if pos:
            self.points.append(pos)
            
            # Calculate velocity if we have previous point
            if len(self.points) >= 2:
                prev = self.points[-2]
                dx = pos[0] - prev[0]
                dy = pos[1] - prev[1]
                self.velocity.append((dx, dy))
            else:
                self.velocity.append((0, 0))
            
            # Limit trail length
            if len(self.points) > self.max_length:
                self.points.pop(0)
                self.velocity.pop(0)
        else:
            # If tracking lost, slowly reduce trail
            if self.points:
                self.points.pop(0)
                if self.velocity:
                    self.velocity.pop(0)

    def draw(self, screen):
        if len(self.points) < 2:
            return

        # Draw glowing trail with enhanced effects
        for i in range(1, len(self.points)):
            p1 = self.points[i-1]
            p2 = self.points[i]
            
            # Progressive thickness towards the tip
            progress = i / len(self.points)
            thickness = int(progress * 14)
            
            # Calculate velocity magnitude for intensity
            if i < len(self.velocity):
                vel_mag = math.sqrt(self.velocity[i][0]**2 + self.velocity[i][1]**2)
                intensity = min(1.0, vel_mag / 20.0)  # Normalize velocity
            else:
                intensity = 1.0
            
            if thickness > 0:
                # Outer glow with intensity-based color
                glow_color = (
                    int(self.color_glow[0] * intensity),
                    int(self.color_glow[1]),
                    int(self.color_glow[2])
                )
                pygame.draw.line(screen, glow_color, p1, p2, thickness + 8)
                
                # Middle glow
                pygame.draw.line(screen, (150, 230, 255), p1, p2, thickness + 4)
                
                # Core trail
                pygame.draw.line(screen, self.color_core, p1, p2, max(1, thickness))
                
                # Connecting circles for smooth joints
                pygame.draw.circle(screen, self.color_core, 
                                 (int(p2[0]), int(p2[1])), 
                                 max(1, thickness // 2))

    def get_slice_segment(self):
        """Returns the last two points to check for collision."""
        if len(self.points) >= 2:
            return self.points[-2], self.points[-1]
        return None
    
    def get_velocity_magnitude(self):
        """Get current velocity magnitude for effects"""
        if self.velocity:
            v = self.velocity[-1]
            return math.sqrt(v[0]**2 + v[1]**2)
        return 0


class ScreenShake:
    def __init__(self):
        self.shake_amount = 0
        self.shake_duration = 0
        self.offset_x = 0
        self.offset_y = 0
    
    def trigger(self, intensity=10, duration=10):
        """Trigger screen shake effect"""
        self.shake_amount = intensity
        self.shake_duration = duration
    
    def update(self):
        """Update shake effect"""
        if self.shake_duration > 0:
            self.shake_duration -= 1
            
            # Calculate shake offset with decay
            decay = self.shake_duration / 10.0
            current_intensity = self.shake_amount * decay
            
            self.offset_x = random.uniform(-current_intensity, current_intensity)
            self.offset_y = random.uniform(-current_intensity, current_intensity)
        else:
            self.offset_x = 0
            self.offset_y = 0
    
    def get_offset(self):
        """Get current shake offset"""
        return (int(self.offset_x), int(self.offset_y))
    
    def apply_to_screen(self, screen, background):
        """Apply shake effect to screen rendering"""
        if self.shake_duration > 0:
            offset = self.get_offset()
            screen.blit(background, offset)
            return True
        else:
            screen.blit(background, (0, 0))
            return False
