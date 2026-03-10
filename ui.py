import pygame
import math
import time

class UI:
    def __init__(self, screen_width, screen_height):
        pygame.font.init()
        self.width = screen_width
        self.height = screen_height
        
        # Load cooler system fonts
        try:
            self.font_title = pygame.font.SysFont('impact', 80)
            self.font_large = pygame.font.SysFont('impact', 60)
            self.font_medium = pygame.font.SysFont('trebuchetms', 40, bold=True)
            self.font_small = pygame.font.SysFont('trebuchetms', 22, bold=True)
        except:
            self.font_title = pygame.font.Font(None, 80)
            self.font_large = pygame.font.Font(None, 60)
            self.font_medium = pygame.font.Font(None, 40)
            self.font_small = pygame.font.Font(None, 24)

    def draw_text(self, screen, text, font, color, center_x, center_y, shadow_offset=3, pulse=False):
        y_offset = 0
        if pulse:
            # Subtle floating / pulsing animation using sine wave based on time
            y_offset = math.sin(time.time() * 5) * 5
            
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(center_x, center_y + y_offset))
        
        # Soft Drop Shadow
        shadow = font.render(text, True, (20, 20, 20))
        shadow_rect = shadow.get_rect(center=(center_x + shadow_offset, center_y + y_offset + shadow_offset))
        screen.blit(shadow, shadow_rect)
        
        screen.blit(surface, rect)

    def draw_start_screen(self, screen):
        # Dark Gradient Overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((10, 15, 30, 180))
        screen.blit(overlay, (0, 0))

        # Title with neon colors
        self.draw_text(screen, "AI FRUIT NINJA", self.font_title, (0, 255, 255), self.width//2, self.height//3 - 30, shadow_offset=5, pulse=True)
        self.draw_text(screen, "PROJECT EXPO", self.font_medium, (255, 100, 200), self.width//2, self.height//3 + 40, shadow_offset=2)
        
        # Instructions
        self.draw_text(screen, "Move index finger to control the blade.", self.font_medium, (255, 255, 255), self.width//2, self.height//2 + 40)
        
        # Blinking start text
        if int(time.time() * 2) % 2 == 0:
            self.draw_text(screen, "[ RAISE HAND TO START ]", self.font_small, (0, 255, 100), self.width//2, self.height - 100)

    def draw_game_over(self, screen, score):
        # Deep Red Overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((50, 5, 5, 200))
        screen.blit(overlay, (0, 0))

        self.draw_text(screen, "GAME OVER", self.font_title, (255, 50, 50), self.width//2, self.height//3, shadow_offset=5, pulse=True)
        self.draw_text(screen, f"FINAL SCORE: {score}", self.font_large, (255, 215, 0), self.width//2, self.height//2 + 20)
        
        if int(time.time() * 2) % 2 == 0:
            self.draw_text(screen, "[ LOWER AND RAISE HAND TO RESTART ]", self.font_small, (200, 200, 200), self.width//2, self.height - 100)

    def draw_hud(self, screen, score, high_score, combo, difficulty=None):
        # Score background panel
        s_panel = pygame.Surface((220, 80), pygame.SRCALPHA)
        pygame.draw.rect(s_panel, (0, 0, 0, 150), s_panel.get_rect(), border_radius=10)
        screen.blit(s_panel, (20, 20))
        
        self.draw_text(screen, f"SCORE: {score}", self.font_medium, (255, 255, 255), 130, 45)
        self.draw_text(screen, f"HIGH: {high_score}", self.font_small, (150, 150, 150), 130, 80)
        
        # Difficulty indicator
        if difficulty:
            diff_colors = {
                "Easy": (0, 255, 100),
                "Medium": (255, 200, 0),
                "Hard": (255, 140, 0),
                "Expert": (255, 80, 80),
                "Master": (200, 0, 255)
            }
            diff_name = difficulty.get('name', 'Easy')
            diff_color = diff_colors.get(diff_name, (255, 255, 255))
            
            diff_panel = pygame.Surface((140, 35), pygame.SRCALPHA)
            pygame.draw.rect(diff_panel, (0, 0, 0, 150), diff_panel.get_rect(), border_radius=8)
            screen.blit(diff_panel, (self.width - 160, 20))
            
            diff_surf = self.font_small.render(diff_name.upper(), True, diff_color)
            diff_rect = diff_surf.get_rect(center=(self.width - 90, 37))
            screen.blit(diff_surf, diff_rect)
        
        # Dynamic combo display with enhanced effects
        if combo > 1:
            combo_scale = min(1.0 + (combo * 0.05), 1.5)
            pulse = math.sin(time.time() * 15) * 3 * combo_scale
            
            # Glow effect for high combos
            if combo >= 5:
                glow_color = (255, 100, 0) if combo >= 10 else (255, 200, 0)
                c_glow = self.font_large.render(f"x{combo} COMBO!", True, glow_color)
                for offset in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
                    c_glow_rect = c_glow.get_rect(center=(self.width//2 + offset[0], 80 + pulse + offset[1]))
                    screen.blit(c_glow, c_glow_rect)
            
            c_text = self.font_large.render(f"x{combo} COMBO!", True, (255, 215, 0))
            c_rect = c_text.get_rect(center=(self.width//2, 80 + pulse))
            screen.blit(c_text, c_rect)

    def draw_expo_mode(self, screen, tracker_stats, fps):
        y_offset = self.height - 120
        
        detected = tracker_stats.get('detected', False)
        conf = tracker_stats.get('confidence', 0.0)

        # Glassmorphic Box
        box_width, box_height = 280, 100
        glass = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(glass, (20, 30, 50, 180), glass.get_rect(), border_radius=12)
        pygame.draw.rect(glass, (100, 200, 255, 100), glass.get_rect(), width=2, border_radius=12) # Glow border
        screen.blit(glass, (15, y_offset))
        
        # Header
        head_text = self.font_small.render("SYSTEM TELEMETRY", True, (150, 200, 255))
        screen.blit(head_text, (30, y_offset + 10))
        pygame.draw.line(screen, (100, 200, 255, 100), (30, y_offset + 35), (270, y_offset + 35))

        # FPS
        color_fps = (0, 255, 100) if fps > 30 else (255, 50, 50)
        fps_surf = self.font_small.render(f"RENDER FPS: {int(fps)}", True, color_fps)
        screen.blit(fps_surf, (30, y_offset + 45))
        
        # Detection Status
        det_text = "TRACKING ACTIVE" if detected else "NO SIGNAL"
        det_color = (0, 255, 100) if detected else (255, 50, 50)
        det_surf = self.font_small.render(f"VISION: {det_text}", True, det_color)
        screen.blit(det_surf, (30, y_offset + 70))
        
        # Confidence Bar
        conf_y = y_offset + 78
        pygame.draw.rect(screen, (50, 50, 50), (180, conf_y, 90, 8), border_radius=4)
        pygame.draw.rect(screen, (0, 200, 255), (180, conf_y, int(90 * conf), 8), border_radius=4)

