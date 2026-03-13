"""Utility helpers for package_name."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import pandas as pd


DataLike = pd.DataFrame | dict[str, list[Any]] | list[dict[str, Any]]


def ensure_dataframe(data: DataLike) -> pd.DataFrame:
    """Return a defensive DataFrame copy from supported inputs."""
    if isinstance(data, pd.DataFrame):
        return data.copy()

    try:
        return pd.DataFrame(data)
    except Exception as exc:
        raise TypeError("data must be convertible to a pandas DataFrame") from exc


def validate_columns(frame: pd.DataFrame, columns: Iterable[str]) -> list[str]:
    """Validate that requested columns exist in the DataFrame."""
    requested = list(columns)
    missing = [column for column in requested if column not in frame.columns]
    if missing:
        missing_text = ", ".join(sorted(missing))
        raise ValueError(f"unknown columns: {missing_text}")
    return requested
