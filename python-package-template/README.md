# Cv-Fruit-Ninja

Cv-Fruit-Ninja is a professional starter template for a PyPI-ready Python library built with modern setuptools packaging.

## Features

- Uses `pyproject.toml` and PEP 621 metadata
- Includes a clean package layout with tests
- Depends on `numpy` and `pandas`
- Builds with `python -m build`
- Ready to publish to PyPI after updating the placeholder metadata

## Installation

```bash
pip install cv-fruit-ninja
```

For local development:

```bash
pip install -e ".[dev]"
```

## Example Usage

```python
from cv_fruit_ninja import summarize_dataframe

summary = summarize_dataframe(
    {
        "sales": [1200, 1350, 1280],
        "cost": [420, 460, 440],
    }
)

print(summary)
```

## Build

```bash
python -m build
```

## Publish to PyPI

```bash
python -m twine upload dist/*
```

Replace the placeholder author and email in `pyproject.toml` before publishing.
