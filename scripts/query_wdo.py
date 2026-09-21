from pathlib import Path

import duckdb

PARQUET_FILE = Path("data/processed/wdo/sample_wdo_1m.parquet")


def main() -> None:
    path = PARQUET_FILE.as_posix()

    result = duckdb.sql(f"""
        SELECT
            COUNT(*) AS candles,
            MIN(timestamp) AS first_candle,
            MAX(timestamp) AS last_candle,
            MIN(low) AS minimum_price,
            MAX(high) AS maximum_price,
            SUM(volume) AS total_volume
        FROM read_parquet('{path}')
        """)

    result.show()


if __name__ == "__main__":
    main()
