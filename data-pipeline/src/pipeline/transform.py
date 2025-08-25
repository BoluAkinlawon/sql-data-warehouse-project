from __future__ import annotations

from typing import Tuple

import pandas as pd

from .config import DATA_PROCESSED_DIR, get_logger


logger = get_logger(__name__)


def _standardize_strings(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "product" in df.columns:
        df["product"] = (
            df["product"].astype(str).str.strip().str.lower().str.replace("\s+", " ", regex=True)
        )
    if "city" in df.columns:
        df["city"] = df["city"].astype(str).str.strip().str.title()
    if "state" in df.columns:
        df["state"] = df["state"].astype(str).str.strip().str.upper()
    return df


def _coerce_types(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Parse date from multiple formats
    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce", infer_datetime_format=True)
    for col in ["order_id", "quantity"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    if "price" in df.columns:
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
    return df


def clean_orders(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = df_raw.copy()
    df = _standardize_strings(df)
    df = _coerce_types(df)

    # Drop invalid rows
    required = ["order_id", "customer_id", "order_date", "product", "quantity", "price"]
    missing_cols = [c for c in required if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    before = len(df)
    df = df.dropna(subset=["order_id", "customer_id", "order_date", "quantity", "price"])  # type: ignore[list-item]
    # Convert NA-aware Int64 to int after dropping NAs
    df["order_id"] = df["order_id"].astype(int)
    df["quantity"] = df["quantity"].astype(int)
    after = len(df)
    dropped = before - after
    if dropped:
        logger.info("Dropped %d invalid rows", dropped)

    # Derive fields
    df["revenue"] = df["quantity"] * df["price"].astype(float)
    df["order_ym"] = df["order_date"].dt.strftime("%Y-%m")

    # Order columns nicely
    prefer = [
        "order_id",
        "customer_id",
        "order_date",
        "order_ym",
        "product",
        "quantity",
        "price",
        "revenue",
        "city",
        "state",
    ]
    cols = [c for c in prefer if c in df.columns] + [c for c in df.columns if c not in prefer]
    df = df[cols]
    return df


def aggregate_revenue_by_state(df_clean: pd.DataFrame) -> pd.DataFrame:
    if "state" not in df_clean.columns:
        raise ValueError("Column 'state' missing in cleaned DataFrame")
    grouped = (
        df_clean.groupby("state", dropna=False)
        .agg(total_revenue=("revenue", "sum"), orders=("order_id", "count"))
        .reset_index()
        .sort_values(["total_revenue", "orders"], ascending=[False, False])
    )
    return grouped


def run_transform_and_save_outputs(df_raw: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df_clean = clean_orders(df_raw)
    df_rev_state = aggregate_revenue_by_state(df_clean)

    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    clean_csv = DATA_PROCESSED_DIR / "orders_clean.csv"
    rev_csv = DATA_PROCESSED_DIR / "revenue_by_state.csv"

    df_clean.to_csv(clean_csv, index=False)
    df_rev_state.to_csv(rev_csv, index=False)
    logger.info("Wrote cleaned data to %s (%d rows)", clean_csv, len(df_clean))
    logger.info("Wrote revenue by state to %s (%d rows)", rev_csv, len(df_rev_state))

    return df_clean, df_rev_state

