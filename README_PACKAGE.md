# AI Fruit Ninja 🥷🍎

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An AI-powered Fruit Ninja game featuring real-time hand tracking with MediaPipe, built with Pygame. Slice fruits with your hand movements captured through your webcam!

## Features

- 🖐️ **Hand Tracking**: Real-time hand detection using MediaPipe
- 🎮 **Dynamic Gameplay**: Progressive difficulty with 5 difficulty tiers
- 💥 **Visual Effects**: Screen shake, particle systems, and glowing sword trails
- 🏆 **Scoring System**: Combo bonuses and high score tracking
- ⚡ **Optimized Performance**: Image caching, efficient collision detection, 60 FPS
- 🎨 **Professional UI**: Difficulty indicators, telemetry panel, smooth animations

## Demo

![AI Fruit Ninja Gameplay](https://via.placeholder.com/800x600?text=Gameplay+Demo)

## Installation

### Method 1: Install from PyPI (Recommended)

```bash
pip install ai-fruit-ninja
```

### Method 2: Install from Source

```bash
# Clone the repository
git clone https://github.com/joedanields/Fruit-Ninja.git
cd Fruit-Ninja

# Install in development mode
pip install -e .
```

### Method 3: Install from Local Build

```bash
# Build the package
python -m build

# Install the wheel
pip install dist/ai_fruit_ninja-1.0.0-py3-none-any.whl
```

## Quick Start

### Run the Game

After installation, simply run:

```bash
ai-fruit-ninja
```

Or use Python module execution:

```bash
python -m ai_fruit_ninja
```

### Use as a Library

```python
from ai_fruit_ninja import run_game

# Start the game
run_game()
```

## Requirements

- Python 3.8 or higher
- Webcam (for hand tracking)
- OpenCV 4.5+
- MediaPipe 0.10+
- Pygame 2.0+
- NumPy < 2.0

## Controls

- 🖐️ **Raise your hand** - Start/Restart game
- 👆 **Move index finger** - Control the blade
- 🖱️ **Mouse fallback** - If hand not detected, use your mouse
- ❌ **Close window** - Exit game

## Gameplay

1. **Start**: Raise your hand to begin
2. **Slice Fruits**: Move your index finger to slice fruits
3. **Avoid Bombs**: Don't slice the bombs!
4. **Build Combos**: Slice multiple fruits quickly for bonus points
5. **Progress**: Game gets harder as your score increases

### Difficulty Tiers

| Tier | Score Required | Bomb Chance | Speed Multiplier |
|------|---------------|-------------|------------------|
| Easy | 0 | 10% | 1.0x |
| Medium | 50 | 15% | 1.2x |
| Hard | 100 | 20% | 1.4x |
| Expert | 200 | 25% | 1.6x |
| Master | 300 | 30% | 1.8x |

### Scoring

- **Fruit Points**: 5-15 points depending on fruit type
- **Combo Bonus**: +2 points per combo level (max +50)
- **Combo Timer**: 0.5 seconds between slices

## Development

### Project Structure

```
ai-fruit-ninja/
├── ai_fruit_ninja/          # Main package directory
│   ├── __init__.py          # Package initialization
│   ├── __main__.py          # Module entry point
│   ├── main.py              # Game loop and entry function
│   ├── game_objects.py      # Fruit, Bomb, GameObject classes
│   ├── mechanics.py         # Game mechanics and physics
│   ├── visuals.py           # Visual effects and rendering
│   ├── hand_tracker.py      # MediaPipe hand tracking
│   ├── ui.py                # User interface
│   ├── config.py            # Game configuration
│   └── assets/              # Game assets (images)
│       ├── watermelon.png
│       ├── apple.png
│       ├── orange.png
│       ├── banana.png
│       ├── bomb.png
│       └── background.jpg
├── README.md                # This file
├── LICENSE                  # MIT License
├── pyproject.toml          # PEP 621 package configuration
├── setup.cfg               # Additional setup configuration
├── MANIFEST.in             # Include non-Python files
└── requirements.txt        # Dependencies

```

### Building from Source

#### Prerequisites

```bash
pip install build twine
```

#### Build the Package

```bash
# Clean previous builds
rm -rf build dist *.egg-info

# Build source distribution and wheel
python -m build
```

This creates:
- `dist/ai_fruit_ninja-1.0.0.tar.gz` (source distribution)
- `dist/ai_fruit_ninja-1.0.0-py3-none-any.whl` (wheel)

#### Install Locally

```bash
# Install in editable mode for development
pip install -e .

# Or install from wheel
pip install dist/ai_fruit_ninja-1.0.0-py3-none-any.whl
```

#### Run Tests (if available)

```bash
pytest tests/
```

### Publishing to PyPI

#### Test PyPI (Recommended First)

```bash
# Upload to Test PyPI
python -m twine upload --repository testpypi dist/*

# Install from Test PyPI to verify
pip install --index-url https://test.pypi.org/simple/ ai-fruit-ninja
```

#### Production PyPI

```bash
# Upload to PyPI
python -m twine upload dist/*

# Verify installation
pip install ai-fruit-ninja
```

## Configuration

The game can be customized by editing `ai_fruit_ninja/config.py`:

### Gameplay Tuning

```python
class GameConfig:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60
    BASE_SPAWN_DELAY = 100
    MIN_SPAWN_DELAY = 30
```

### Visual Effects

```python
class PerformanceConfig:
    ENABLE_PARTICLE_EFFECTS = True
    ENABLE_SCREEN_SHAKE = True
    ENABLE_GLOW_EFFECTS = True
```

### Hand Tracking

```python
class GameConfig:
    HAND_SMOOTHING_FACTOR = 0.4
    HAND_MODEL_COMPLEXITY = 0
    FRAME_SKIP = 2
```

## Technical Highlights

### Performance Optimizations

- ✅ **Image Rotation Caching**: 80% reduction in rotation calculations
- ✅ **Efficient Collision Detection**: Optimized line-circle intersection
- ✅ **Batch Object Removal**: Single-pass object cleanup
- ✅ **Frame Skipping**: Process every 2nd camera frame
- ✅ **Thread-Safe Hand Tracking**: Concurrent camera processing

### Code Quality

- ✅ **Type Hints**: Enhanced code clarity and IDE support
- ✅ **Modular Architecture**: Clean separation of concerns
- ✅ **Resource Management**: Proper asset loading and cleanup
- ✅ **PEP 621 Compliant**: Modern Python packaging standards
- ✅ **Cross-Platform**: Works on Windows, macOS, and Linux

## Troubleshooting

### Common Issues

#### Camera Not Working

```python
# Check camera index in config
CAMERA_INDEX = 0  # Try 0, 1, or 2
```

#### NumPy Version Error

```bash
# Downgrade NumPy if needed
pip install "numpy<2.0"
```

#### MediaPipe Installation Issues

```bash
# Use specific version
pip install mediapipe==0.10.11
```

#### Assets Not Loading

The package uses `importlib.resources` for asset loading. If issues occur:
1. Ensure all assets are in `ai_fruit_ninja/assets/`
2. Verify MANIFEST.in includes all asset files
3. Reinstall the package: `pip install --force-reinstall .`

## Contributing

Contributions are welcome! Areas for improvement:

- Additional fruit types and visual effects
- Sound effects and background music
- Multi-hand tracking for multiplayer
- Gesture recognition for special moves
- Mobile device support
- Additional game modes

### Development Setup

```bash
# Clone repository
git clone https://github.com/joedanields/Fruit-Ninja.git
cd Fruit-Ninja

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run the game
ai-fruit-ninja
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **MediaPipe** - Google's ML framework for hand tracking
- **Pygame** - Game development library
- **OpenCV** - Computer vision library
- Original Fruit Ninja game by Halfbrick Studios

## Author

**Joe Danields**
- GitHub: [@joedanields](https://github.com/joedanields)
- Email: joedanields@example.com

## Support

If you encounter any issues or have questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Search [existing issues](https://github.com/joedanields/Fruit-Ninja/issues)
3. Create a [new issue](https://github.com/joedanields/Fruit-Ninja/issues/new)

---

**Built with ❤️ using Python, MediaPipe, and Pygame**

*Optimized for Project Expo - Showcasing AI, Computer Vision, and Game Development*
