# Quick Start Guide - AI Fruit Ninja

## Installation

Choose one of the following methods:

### Option 1: Install from PyPI (Coming Soon)
```bash
pip install ai-fruit-ninja
```

### Option 2: Install from Source
```bash
git clone https://github.com/joedanields/Fruit-Ninja.git
cd Fruit-Ninja
pip install .
```

### Option 3: Development Installation
```bash
git clone https://github.com/joedanields/Fruit-Ninja.git
cd Fruit-Ninja
pip install -e .
```

## Running the Game

### Method 1: CLI Command
```bash
ai-fruit-ninja
```

### Method 2: Python Module
```bash
python -m ai_fruit_ninja
```

### Method 3: Python Script
```python
from ai_fruit_ninja import run_game
run_game()
```

## Building and Testing

### Build the Package
```bash
# Using build script
python build_package.py

# Or manually
python -m build
```

### Test Installation
```bash
python test_installation.py
```

### Install Locally
```bash
# Install from wheel
pip install dist/ai_fruit_ninja-1.0.0-py3-none-any.whl

# Or editable mode for development
pip install -e .
```

## Troubleshooting

### Issue: Command 'ai-fruit-ninja' not found
**Solution**: Make sure package is installed and Python scripts directory is in PATH
```bash
pip install -e .
# or
pip install .
```

### Issue: Assets not loading
**Solution**: Reinstall package
```bash
pip install --force-reinstall .
```

### Issue: Camera not working
**Solution**: Check camera permissions and index
```python
# Try different camera indices in config.py
CAMERA_INDEX = 0  # or 1, 2
```

### Issue: NumPy version conflict
**Solution**: Downgrade NumPy
```bash
pip install "numpy<2.0"
```

## Publishing (For Maintainers)

### Prerequisites
```bash
pip install build twine
```

### Build
```bash
python -m build
```

### Upload to Test PyPI
```bash
python -m twine upload --repository testpypi dist/*
```

### Upload to PyPI
```bash
python -m twine upload dist/*
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/joedanields/Fruit-Ninja/issues
- Email: joedanields@example.com
