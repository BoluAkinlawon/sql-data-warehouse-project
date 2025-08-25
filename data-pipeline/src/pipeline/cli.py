from __future__ import annotations

import argparse
import sys
import time

from .config import ensure_data_dirs_exist, get_logger
from .ingest import generate_sample_csv, read_raw_csv
from .transform import run_transform_and_save_outputs
from .load import run_load


logger = get_logger(__name__)


def _cmd_ingest(_: argparse.Namespace) -> int:
    ensure_data_dirs_exist()
    path = generate_sample_csv()
    logger.info("Ingest complete: %s", path)
    return 0


def _cmd_transform(_: argparse.Namespace) -> int:
    df_raw = read_raw_csv()
    run_transform_and_save_outputs(df_raw)
    logger.info("Transform complete")
    return 0


def _cmd_load(_: argparse.Namespace) -> int:
    run_load()
    logger.info("Load complete")
    return 0


def _cmd_run(_: argparse.Namespace) -> int:
    start = time.time()
    ensure_data_dirs_exist()
    logger.info("Starting ETL run")
    _ = generate_sample_csv()
    df_raw = read_raw_csv()
    run_transform_and_save_outputs(df_raw)
    run_load()
    logger.info("ETL run finished in %.2fs", time.time() - start)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simple ETL pipeline CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("ingest", help="Generate/read raw CSV").set_defaults(func=_cmd_ingest)
    sub.add_parser("transform", help="Clean and aggregate data").set_defaults(func=_cmd_transform)
    sub.add_parser("load", help="Load outputs to SQLite and Parquet").set_defaults(func=_cmd_load)
    sub.add_parser("run", help="Run full ETL").set_defaults(func=_cmd_run)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

