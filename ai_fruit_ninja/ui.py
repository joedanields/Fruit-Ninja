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

    def draw_name_input_screen(self, screen, player_name="", cursor_visible=True):
        """Draw name input screen"""
        # Dark overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((10, 15, 30, 200))
        screen.blit(overlay, (0, 0))

        # Title
        self.draw_text(screen, "AI FRUIT NINJA", self.font_title, (0, 255, 255), 
                      self.width//2, self.height//4, shadow_offset=5, pulse=True)
        
        # Instructions
        self.draw_text(screen, "ENTER YOUR NAME", self.font_large, (255, 255, 255), 
                      self.width//2, self.height//2 - 80)
        
        # Name input box
        box_width = 400
        box_height = 60
        box_x = (self.width - box_width) // 2
        box_y = self.height // 2
        
        # Box background
        box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(box_surface, (30, 40, 60, 200), box_surface.get_rect(), border_radius=10)
        pygame.draw.rect(box_surface, (0, 255, 255, 150), box_surface.get_rect(), width=3, border_radius=10)
        screen.blit(box_surface, (box_x, box_y))
        
        # Display name with cursor
        display_text = player_name
        if cursor_visible and int(time.time() * 2) % 2 == 0:
            display_text += "|"
        
        name_surface = self.font_medium.render(display_text or "...", True, (255, 255, 255))
        name_rect = name_surface.get_rect(center=(self.width//2, box_y + box_height//2))
        screen.blit(name_surface, name_rect)
        
        # Instructions
        self.draw_text(screen, "Type your name and press ENTER", self.font_small, 
                      (150, 200, 255), self.width//2, box_y + 100)
        self.draw_text(screen, "Press ESC to use 'Player'", self.font_small, 
                      (150, 150, 150), self.width//2, box_y + 130)

    def draw_leaderboard(self, screen, leaderboard_data, current_score=None, current_rank=None, player_name=""):
        """Draw leaderboard screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((10, 15, 30, 220))
        screen.blit(overlay, (0, 0))

        # Title
        self.draw_text(screen, "🏆 LEADERBOARD 🏆", self.font_title, (255, 215, 0), 
                      self.width//2, 80, shadow_offset=5, pulse=True)
        
        # Show current score if provided
        if current_score is not None and current_rank:
            rank_text = f"#{current_rank}" if current_rank else "Not in Top 10"
            rank_color = (0, 255, 100) if current_rank and current_rank <= 3 else (255, 200, 0)
            
            self.draw_text(screen, f"Your Score: {current_score}", self.font_large, 
                          (255, 255, 255), self.width//2, 150)
            self.draw_text(screen, f"Rank: {rank_text}", self.font_medium, 
                          rank_color, self.width//2, 200)
            
            start_y = 260
        else:
            start_y = 160
        
        # Leaderboard header
        header_y = start_y
        self.draw_text(screen, "RANK", self.font_small, (100, 200, 255), 
                      self.width//2 - 200, header_y)
        self.draw_text(screen, "PLAYER", self.font_small, (100, 200, 255), 
                      self.width//2 - 50, header_y)
        self.draw_text(screen, "SCORE", self.font_small, (100, 200, 255), 
                      self.width//2 + 120, header_y)
        
        # Divider line
        pygame.draw.line(screen, (100, 200, 255), 
                        (self.width//2 - 250, header_y + 20), 
                        (self.width//2 + 250, header_y + 20), 2)
        
        # Display top scores
        entry_y = header_y + 40
        for i, entry in enumerate(leaderboard_data[:10], 1):
            # Medal colors for top 3
            if i == 1:
                rank_color = (255, 215, 0)  # Gold
                medal = "🥇"
            elif i == 2:
                rank_color = (192, 192, 192)  # Silver
                medal = "🥈"
            elif i == 3:
                rank_color = (205, 127, 50)  # Bronze
                medal = "🥉"
            else:
                rank_color = (150, 150, 150)
                medal = f"#{i}"
            
            # Highlight current player's entry
            is_current = (entry['name'] == player_name and 
                         current_score is not None and 
                         entry['score'] == current_score)
            
            if is_current:
                # Highlight background
                highlight = pygame.Surface((500, 35), pygame.SRCALPHA)
                pygame.draw.rect(highlight, (0, 255, 100, 30), highlight.get_rect(), border_radius=5)
                screen.blit(highlight, (self.width//2 - 250, entry_y - 5))
            
            text_color = (255, 255, 0) if is_current else (255, 255, 255)
            
            # Rank
            rank_surf = self.font_small.render(medal, True, rank_color)
            rank_rect = rank_surf.get_rect(center=(self.width//2 - 200, entry_y + 10))
            screen.blit(rank_surf, rank_rect)
            
            # Player name (truncate if too long)
            name_display = entry['name'][:15] if len(entry['name']) > 15 else entry['name']
            name_surf = self.font_small.render(name_display, True, text_color)
            name_rect = name_surf.get_rect(midleft=(self.width//2 - 150, entry_y + 10))
            screen.blit(name_surf, name_rect)
            
            # Score
            score_surf = self.font_small.render(str(entry['score']), True, text_color)
            score_rect = score_surf.get_rect(center=(self.width//2 + 120, entry_y + 10))
            screen.blit(score_surf, score_rect)
            
            # Max combo (small)
            if entry.get('max_combo', 0) > 0:
                combo_text = f"x{entry['max_combo']}"
                combo_surf = pygame.font.SysFont('trebuchetms', 14).render(combo_text, True, (255, 200, 0))
                combo_rect = combo_surf.get_rect(midleft=(self.width//2 + 170, entry_y + 10))
                screen.blit(combo_surf, combo_rect)
            
            entry_y += 38
        
        # Instructions at bottom
        if int(time.time() * 2) % 2 == 0:
            self.draw_text(screen, "[ PRESS SPACE TO PLAY AGAIN ]", self.font_small, 
                          (0, 255, 100), self.width//2, self.height - 80)
        self.draw_text(screen, "Press ESC to quit", self.font_small, 
                      (150, 150, 150), self.width//2, self.height - 50)

    def draw_waiting_for_hand(self, screen):
        """Draw waiting for hand detection screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((10, 15, 30, 150))
        screen.blit(overlay, (0, 0))

        # Animated message
        pulse_scale = 1.0 + math.sin(time.time() * 3) * 0.1
        
        self.draw_text(screen, "READY TO PLAY!", self.font_large, (0, 255, 255), 
                      self.width//2, self.height//2 - 80, shadow_offset=5, pulse=True)
        
        # Hand icon simulation or text
        self.draw_text(screen, "👋", self.font_title, (255, 255, 255), 
                      self.width//2, self.height//2 - 10)
        
        if int(time.time() * 3) % 3 == 0:
            msg = "Detecting hand..."
        elif int(time.time() * 3) % 3 == 1:
            msg = "Raise your hand..."
        else:
            msg = "Show index finger..."
        
        self.draw_text(screen, msg, self.font_medium, (255, 200, 0), 
                      self.width//2, self.height//2 + 60)
        
        self.draw_text(screen, "Game will start automatically", self.font_small, 
                      (150, 200, 255), self.width//2, self.height//2 + 120)
