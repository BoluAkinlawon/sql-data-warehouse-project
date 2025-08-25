from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from .config import DATA_PROCESSED_DIR, SQLITE_DB_PATH, get_logger


logger = get_logger(__name__)


def _read_processed() -> tuple[pd.DataFrame, pd.DataFrame]:
    clean_csv = DATA_PROCESSED_DIR / "orders_clean.csv"
    rev_csv = DATA_PROCESSED_DIR / "revenue_by_state.csv"
    if not clean_csv.exists() or not rev_csv.exists():
        raise FileNotFoundError(
            f"Expected processed CSVs at {clean_csv} and {rev_csv}. Run transform step first."
        )
    return pd.read_csv(clean_csv), pd.read_csv(rev_csv)


def write_parquet(df_clean: pd.DataFrame) -> Path:
    out_path = DATA_PROCESSED_DIR / "orders_clean.parquet"
    df_clean.to_parquet(out_path, index=False)
    logger.info("Wrote Parquet to %s (%d rows)", out_path, len(df_clean))
    return out_path


def write_sqlite(df_clean: pd.DataFrame, df_rev_state: pd.DataFrame) -> Path:
    SQLITE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(SQLITE_DB_PATH) as conn:
        df_clean.to_sql("orders", conn, if_exists="replace", index=False)
        df_rev_state.to_sql("revenue_by_state", conn, if_exists="replace", index=False)
    logger.info("Loaded tables into SQLite at %s", SQLITE_DB_PATH)
    return SQLITE_DB_PATH


def run_load() -> tuple[Path, Path]:
    df_clean, df_rev_state = _read_processed()
    parquet_path = write_parquet(df_clean)
    sqlite_path = write_sqlite(df_clean, df_rev_state)
    return parquet_path, sqlite_path

