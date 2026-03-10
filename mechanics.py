import math
import time

class ScoreSystem:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.combo_count = 0
        self.last_slice_time = 0
        self.combo_threshold = 0.5  # Seconds for combo
        self.font_color = (255, 255, 255)

    def add_score(self, points):
        current_time = time.time()
        
        # Combo logic
        if current_time - self.last_slice_time < self.combo_threshold:
            self.combo_count += 1
            bonus = self.combo_count * 2
            total_points = points + bonus
        else:
            self.combo_count = 1
            total_points = points
            
        self.score += total_points
        self.last_slice_time = current_time
        
        if self.score > self.high_score:
            self.high_score = self.score

    def reset(self):
        self.score = 0
        self.combo_count = 0
        self.last_slice_time = 0

class GameEngine:
    @staticmethod
    def check_collision(p1, p2, circle_center, radius):
        """
        Line to circle collision detection.
        Checks if the line segment from p1 to p2 intersects the circle.
        p1, p2, circle_center: (x, y) tuples
        radius: int/float
        """
        x1, y1 = p1
        x2, y2 = p2
        cx, cy = circle_center

        # Vector from p1 to p2
        dx, dy = x2 - x1, y2 - y1
        # Vector from p1 to circle center
        fx, fy = x1 - cx, y1 - cy

        a = dx * dx + dy * dy
        b = 2 * (fx * dx + fy * dy)
        c = (fx * fx + fy * fy) - radius * radius

        if a == 0:
            return False

        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return False
            
        discriminant = math.sqrt(discriminant)
        
        # t1 and t2 are the points of intersection on the line (between 0.0 and 1.0)
        t1 = (-b - discriminant) / (2 * a)
        t2 = (-b + discriminant) / (2 * a)

        # Check if the intersection points are within the line segment
        if (0 <= t1 <= 1) or (0 <= t2 <= 1):
            return True
            
        return False
