from pathlib import Path

import polars as pl

RAW_FILE = Path("data/raw/wdo/sample_wdo_1m.csv")
PROCESSED_FILE = Path("data/processed/wdo/sample_wdo_1m.parquet")


def load_raw_data(path: Path) -> pl.DataFrame:
    return pl.read_csv(path)


def normalize_data(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pl.col("timestamp").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S", strict=True),
        pl.col("open").cast(pl.Float64),
        pl.col("high").cast(pl.Float64),
        pl.col("low").cast(pl.Float64),
        pl.col("close").cast(pl.Float64),
        pl.col("volume").cast(pl.Int64),
    ).sort("timestamp")


def validate_data(df: pl.DataFrame) -> None:
    invalid_rows = df.filter(
        (pl.col("high") < pl.max_horizontal("open", "close"))
        | (pl.col("low") > pl.min_horizontal("open", "close"))
        | (pl.col("volume") < 0)
    )

    if invalid_rows.height > 0:
        raise ValueError("Foram encontrados candles inválidos.")


def save_parquet(df: pl.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(path)


def main() -> None:
    raw_data = load_raw_data(RAW_FILE)
    normalized_data = normalize_data(raw_data)
    validate_data(normalized_data)
    save_parquet(normalized_data, PROCESSED_FILE)

    print(normalized_data)
    print(f"\nArquivo criado em: {PROCESSED_FILE}")


if __name__ == "__main__":
    main()
