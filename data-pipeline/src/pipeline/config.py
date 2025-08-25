from __future__ import annotations

import logging
import os
from pathlib import Path


def _resolve_project_root() -> Path:
    # src/pipeline/config.py -> parents[0]=pipeline, [1]=src, [2]=project root
    return Path(__file__).resolve().parents[2]


PROJECT_ROOT: Path = _resolve_project_root()
DATA_DIR: Path = PROJECT_ROOT / "data"
DATA_RAW_DIR: Path = DATA_DIR / "raw"
DATA_PROCESSED_DIR: Path = DATA_DIR / "processed"
SQLITE_DB_PATH: Path = DATA_PROCESSED_DIR / "orders.sqlite"


def ensure_data_dirs_exist() -> None:
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def get_logger(name: str = "pipeline") -> logging.Logger:
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        handler.setFormatter(logging.Formatter(fmt))
        logger.addHandler(handler)
    return logger
