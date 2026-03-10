import math
import time

class ScoreSystem:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.combo_count = 0
        self.max_combo = 0
        self.last_slice_time = 0
        self.combo_threshold = 0.5  # Seconds for combo
        self.total_slices = 0
        self.font_color = (255, 255, 255)

    def add_score(self, points):
        current_time = time.time()
        
        # Combo logic with enhanced feedback
        if current_time - self.last_slice_time < self.combo_threshold:
            self.combo_count += 1
            # Progressive combo bonus
            bonus = min(self.combo_count * 2, 50)  # Cap bonus at 50
            total_points = points + bonus
        else:
            self.combo_count = 1
            total_points = points
        
        # Update max combo
        if self.combo_count > self.max_combo:
            self.max_combo = self.combo_count
            
        self.score += total_points
        self.total_slices += 1
        self.last_slice_time = current_time
        
        if self.score > self.high_score:
            self.high_score = self.score

    def get_accuracy(self, total_spawned):
        """Calculate slice accuracy percentage"""
        if total_spawned == 0:
            return 0
        return int((self.total_slices / total_spawned) * 100)

    def reset(self):
        self.score = 0
        self.combo_count = 0
        self.last_slice_time = 0
        self.total_slices = 0
        # Don't reset high_score and max_combo - keep across games


class DifficultyManager:
    """Manages game difficulty progression"""
    
    # Difficulty tiers
    TIERS = {
        0: {"name": "Easy", "bomb_chance": 0.10, "speed_mult": 1.0},
        50: {"name": "Medium", "bomb_chance": 0.15, "speed_mult": 1.2},
        100: {"name": "Hard", "bomb_chance": 0.20, "speed_mult": 1.4},
        200: {"name": "Expert", "bomb_chance": 0.25, "speed_mult": 1.6},
        300: {"name": "Master", "bomb_chance": 0.30, "speed_mult": 1.8}
    }
    
    @staticmethod
    def get_difficulty(score):
        """Get current difficulty tier based on score"""
        current_tier = None
        for threshold in sorted(DifficultyManager.TIERS.keys(), reverse=True):
            if score >= threshold:
                current_tier = DifficultyManager.TIERS[threshold].copy()
                current_tier['threshold'] = threshold
                return current_tier
        # Default to easiest
        tier = DifficultyManager.TIERS[0].copy()
        tier['threshold'] = 0
        return tier
    
    @staticmethod
    def get_bomb_chance(score):
        """Get dynamic bomb spawn chance based on score"""
        return DifficultyManager.get_difficulty(score)['bomb_chance']
    
    @staticmethod
    def get_speed_multiplier(score):
        """Get speed multiplier for spawn rate"""
        return DifficultyManager.get_difficulty(score)['speed_mult']


class GameEngine:
    # Cache for collision calculations
    _collision_cache = {}
    _cache_max_size = 1000
    
    @staticmethod
    def check_collision(p1, p2, circle_center, radius):
        """
        Optimized line to circle collision detection.
        Checks if the line segment from p1 to p2 intersects the circle.
        p1, p2, circle_center: (x, y) tuples
        radius: int/float
        """
        x1, y1 = p1
        x2, y2 = p2
        cx, cy = circle_center

        # Vector from p1 to p2
        dx = x2 - x1
        dy = y2 - y1
        
        # Vector from p1 to circle center
        fx = x1 - cx
        fy = y1 - cy

        a = dx * dx + dy * dy
        
        # Early exit if line segment has no length
        if a < 0.001:
            # Check if point is inside circle
            dist_sq = fx * fx + fy * fy
            return dist_sq <= radius * radius
        
        b = 2 * (fx * dx + fy * dy)
        c = (fx * fx + fy * fy) - radius * radius

        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return False
        
        # Use math.sqrt only once
        sqrt_disc = math.sqrt(discriminant)
        
        # t1 and t2 are the points of intersection on the line (between 0.0 and 1.0)
        two_a = 2 * a
        t1 = (-b - sqrt_disc) / two_a
        t2 = (-b + sqrt_disc) / two_a

        # Check if the intersection points are within the line segment
        return (0 <= t1 <= 1) or (0 <= t2 <= 1)
