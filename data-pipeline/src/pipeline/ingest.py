from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd

from .config import DATA_RAW_DIR, ensure_data_dirs_exist, get_logger


logger = get_logger(__name__)


def generate_sample_csv(output_path: Optional[Path] = None) -> Path:
    ensure_data_dirs_exist()
    out_path = output_path or (DATA_RAW_DIR / "orders.csv")

    # Synthetic, slightly messy records for learning
    rows = [
        {
            "order_id": 1,
            "customer_id": "C001",
            "order_date": "2024-12-31",
            "product": "   Widget A",
            "quantity": 2,
            "price": 9.99,
            "city": "seattle ",
            "state": "wa",
        },
        {
            "order_id": 2,
            "customer_id": "C002",
            "order_date": "2025/01/02",
            "product": "widget b",
            "quantity": 1,
            "price": 19.5,
            "city": "PORTLAND",
            "state": "OR",
        },
        {
            "order_id": 3,
            "customer_id": "C003",
            "order_date": "01-05-2025",
            "product": "Gadget C",
            "quantity": 5,
            "price": 4.0,
            "city": " San Francisco",
            "state": " ca ",
        },
        {
            "order_id": 4,
            "customer_id": None,  # will be dropped as invalid
            "order_date": "2025-01-07",
            "product": "Widget A",
            "quantity": 3,
            "price": 9.99,
            "city": "seattle",
            "state": "WA",
        },
    ]

    df = pd.DataFrame(rows)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    logger.info("Generated sample CSV at %s (%d rows)", out_path, len(df))
    return out_path


def read_raw_csv(input_path: Optional[Path] = None) -> pd.DataFrame:
    ensure_data_dirs_exist()
    path = input_path or (DATA_RAW_DIR / "orders.csv")
    if not path.exists():
        logger.warning("Raw CSV %s not found; generating sample.", path)
        generate_sample_csv(path)
    df = pd.read_csv(path)
    logger.info("Read raw CSV from %s (%d rows)", path, len(df))
    return df
