"""Core functionality for package_name."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from .utils import DataLike, ensure_dataframe, validate_columns


@dataclass(slots=True)
class DataAnalyzer:
    """Analyze numeric columns in a pandas DataFrame."""

    frame: pd.DataFrame

    @classmethod
    def from_data(cls, data: DataLike) -> "DataAnalyzer":
        """Build an analyzer from supported in-memory data."""
        return cls(frame=ensure_dataframe(data))

    def summarize(self, columns: list[str] | None = None) -> pd.DataFrame:
        """Return count, mean, min, max, and range for numeric columns."""
        frame = self.frame
        if columns is not None:
            frame = frame[validate_columns(frame, columns)]

        numeric_frame = frame.select_dtypes(include=[np.number])
        if numeric_frame.empty:
            raise ValueError("at least one numeric column is required")

        summary = numeric_frame.agg(["count", "mean", "min", "max"]).T
        summary["range"] = summary["max"] - summary["min"]
        return summary.sort_index()


def summarize_dataframe(data: DataLike, columns: list[str] | None = None) -> pd.DataFrame:
    """Convenience wrapper for summarizing tabular data."""
    analyzer = DataAnalyzer.from_data(data)
    return analyzer.summarize(columns=columns)
