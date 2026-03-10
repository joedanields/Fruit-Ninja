"""
Game Configuration File
Centralized configuration for easy tuning of game parameters
"""

class GameConfig:
    """Main game configuration"""
    
    # Display Settings
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60
    WINDOW_TITLE = "AI Fruit Ninja - Project Expo"
    
    # Background Settings
    BACKGROUND_IMAGE = "assets/background.jpg"
    BACKGROUND_COLOR = (20, 20, 40)  # Fallback color if image not found
    
    # Gameplay Settings
    BASE_SPAWN_DELAY = 100  # Starting spawn delay (frames)
    MIN_SPAWN_DELAY = 30    # Minimum spawn delay (fastest possible)
    SPAWN_SPEED_INCREASE = 0.5  # How much faster spawning gets per point
    MAX_OBJECTS = 30  # Prevent too many objects on screen
    
    # Collision Settings
    COLLISION_RADIUS_FACTOR = 0.8  # Makes collision more precise (0.8 = 80% of radius)
    
    # Object Physics
    GRAVITY = 0.4
    VELOCITY_X_RANGE = (-3, 3)
    VELOCITY_Y_RANGE = (-14, -18)
    ROTATION_SPEED_RANGE = (-5, 5)
    
    # Scoring Settings
    COMBO_THRESHOLD = 0.5  # Seconds between slices to maintain combo
    COMBO_BONUS_PER_HIT = 2  # Points added per combo level
    MAX_COMBO_BONUS = 50  # Maximum combo bonus points
    
    # Difficulty Tiers (score_threshold: settings)
    DIFFICULTY_TIERS = {
        0:   {"name": "Easy",   "bomb_chance": 0.10, "speed_mult": 1.0},
        50:  {"name": "Medium", "bomb_chance": 0.15, "speed_mult": 1.2},
        100: {"name": "Hard",   "bomb_chance": 0.20, "speed_mult": 1.4},
        200: {"name": "Expert", "bomb_chance": 0.25, "speed_mult": 1.6},
        300: {"name": "Master", "bomb_chance": 0.30, "speed_mult": 1.8}
    }
    
    # Visual Effects
    SWORD_TRAIL_LENGTH = 12
    SWORD_CORE_COLOR = (255, 255, 255)
    SWORD_GLOW_COLOR = (0, 255, 255)
    
    PARTICLE_COUNT_FRUIT = 20
    PARTICLE_COUNT_BOMB = 50
    BOMB_EXPLOSION_COLOR = (255, 100, 0)
    
    SCREEN_SHAKE_INTENSITY = 15
    SCREEN_SHAKE_DURATION = 15  # frames
    
    # Hand Tracking Settings
    CAMERA_INDEX = 0
    HAND_SMOOTHING_FACTOR = 0.4
    HAND_DETECTION_CONFIDENCE = 0.7
    HAND_TRACKING_CONFIDENCE = 0.7
    HAND_MODEL_COMPLEXITY = 0  # 0 = lite, 1 = full
    
    CAMERA_WIDTH = 640
    CAMERA_HEIGHT = 480
    CAMERA_FPS = 30
    FRAME_SKIP = 2  # Process every Nth frame for performance
    
    # Fruit Types Configuration
    FRUIT_TYPES = {
        'watermelon': {
            'points': 10,
            'image': 'assets/watermelon.png',
            'color': (220, 20, 40),
            'radius': 40
        },
        'apple': {
            'points': 5,
            'image': 'assets/apple.png',
            'color': (220, 20, 20),
            'radius': 40
        },
        'orange': {
            'points': 7,
            'image': 'assets/orange.png',
            'color': (255, 140, 0),
            'radius': 40
        },
        'banana': {
            'points': 15,
            'image': 'assets/banana.png',
            'color': (255, 225, 0),
            'radius': 40
        }
    }
    
    # Bomb Configuration
    BOMB_RADIUS = 35
    BOMB_IMAGE = 'assets/bomb.png'
    
    # UI Colors
    UI_PRIMARY_COLOR = (0, 255, 255)
    UI_SECONDARY_COLOR = (255, 100, 200)
    UI_SUCCESS_COLOR = (0, 255, 100)
    UI_ERROR_COLOR = (255, 50, 50)
    UI_WARNING_COLOR = (255, 200, 0)
    
    DIFFICULTY_COLORS = {
        "Easy": (0, 255, 100),
        "Medium": (255, 200, 0),
        "Hard": (255, 140, 0),
        "Expert": (255, 80, 80),
        "Master": (200, 0, 255)
    }


class PerformanceConfig:
    """Performance optimization settings"""
    
    # Caching
    ROTATION_CACHE_LIMIT = 200
    ROTATION_CACHE_ANGLE_STEP = 5  # Cache every N degrees
    
    # Threading
    THREAD_TIMEOUT = 1.0  # seconds
    
    # Rendering
    ENABLE_PARTICLE_EFFECTS = True
    ENABLE_SCREEN_SHAKE = True
    ENABLE_GLOW_EFFECTS = True
    
    # Debug
    SHOW_FPS = True
    SHOW_TELEMETRY = True
    ENABLE_MOUSE_FALLBACK = True  # Allow mouse control when hand not detected


class DevelopmentConfig:
    """Development and debugging settings"""
    
    DEBUG_MODE = False
    SHOW_COLLISION_BOXES = False
    SHOW_HAND_LANDMARKS = False
    LOG_PERFORMANCE = False
    
    # Cheats for testing
    GOD_MODE = False  # Ignore bomb collisions
    INFINITE_SPAWNS = False  # Don't limit object count
    INSTANT_START = False  # Skip start screen


# Global config instance
config = GameConfig()
perf_config = PerformanceConfig()
dev_config = DevelopmentConfig()
