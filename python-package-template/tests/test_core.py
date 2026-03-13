import pandas as pd
import pytest

from package_name.core import DataAnalyzer, summarize_dataframe


def test_summarize_dataframe_returns_expected_metrics():
    data = pd.DataFrame({"sales": [10, 15, 20], "cost": [4, 5, 6]})

    summary = summarize_dataframe(data)

    assert list(summary.columns) == ["count", "mean", "min", "max", "range"]
    assert summary.loc["sales", "mean"] == pytest.approx(15.0)
    assert summary.loc["cost", "range"] == pytest.approx(2.0)


def test_data_analyzer_rejects_unknown_columns():
    analyzer = DataAnalyzer.from_data({"sales": [10, 12, 14]})

    with pytest.raises(ValueError, match="unknown columns"):
        analyzer.summarize(columns=["profit"])
