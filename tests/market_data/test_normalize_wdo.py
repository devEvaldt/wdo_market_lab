from datetime import datetime

import polars as pl
import pytest

from wdo_market_lab.market_data.normalization.normalize_wdo import (
    normalize_data,
    save_parquet,
    validate_data,
)


def test_normalize_data() -> None:
    df = pl.DataFrame(
        {
            "timestamp": ["2026-08-20 10:01:00", "2026-08-20 10:00:00"],
            "open": [5402.5, 5400.0],
            "high": [5405.0, 5403.0],
            "low": [5401.0, 5399.5],
            "close": [5404.0, 5402.5],
            "volume": [1480, 1250],
        }
    )

    result = normalize_data(df)

    assert result.schema["timestamp"] == pl.Datetime
    assert result.schema["open"] == pl.Float64
    assert result.schema["volume"] == pl.Int64
    assert result["timestamp"][0] == datetime(2026, 8, 20, 10, 0)


def test_validate_data_accepts_valid_candle() -> None:
    df = pl.DataFrame(
        { 
            "timestamp": [datetime(2026, 8, 20, 10, 0)],
            "open": [5400.0],
            "high": [5403.0],
            "low": [5399.5],
            "close": [5402.5],
            "volume": [1250],
        }
    )

    validate_data(df)


def test_validate_data_rejects_invalid_high() -> None:
    df = pl.DataFrame(
        {
            "timestamp": [datetime(2026, 8, 20, 10, 0)],
            "open": [5400.0],
            "high": [5399.0],
            "low": [5398.0],
            "close": [5401.0],
            "volume": [1250],
        }
    )

    with pytest.raises(ValueError, match="Foram encontrados candles inválidos."):
        validate_data(df)


def test_validate_data_rejects_negative_volume() -> None:
    df = pl.DataFrame(
        {
            "timestamp": [datetime(2026, 8, 20, 10, 0)],
            "open": [5400.0],
            "high": [5403.0],
            "low": [5399.0],
            "close": [5402.0],
            "volume": [-100],
        }
    )

    with pytest.raises(ValueError, match="Foram encontrados candles inválidos."):
        validate_data(df)


def test_save_parquet(tmp_path) -> None:
    df = pl.DataFrame(
        {
            "timestamp": [datetime(2026, 8, 20, 10, 0)],
            "open": [5400.0],
            "high": [5403.0],
            "low": [5399.5],
            "close": [5402.5],
            "volume": [1250],
        }
    )

    output_file = tmp_path / "wdo.parquet"

    save_parquet(df, output_file)

    assert output_file.exists()

    saved_data = pl.read_parquet(output_file)

    assert saved_data.height == 1
    assert saved_data["close"][0] == 5402.5