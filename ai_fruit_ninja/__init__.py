"""
AI Fruit Ninja - Hand Tracking Fruit Slicing Game
==================================================

A modern implementation of Fruit Ninja using computer vision and hand tracking.
Built with MediaPipe for hand detection and Pygame for rendering.

Features:
- Real-time hand tracking using MediaPipe
- Dynamic difficulty progression
- Screen shake and particle effects
- Combo system with bonuses
- Performance optimizations (image caching, efficient collision detection)

Usage:
    >>> from ai_fruit_ninja import run_game
    >>> run_game()

CLI:
    $ ai-fruit-ninja
"""

__version__ = "1.0.0"
__author__ = "Joe Danields"
__license__ = "MIT"

from .main import run_game

__all__ = ["run_game", "__version__"]
