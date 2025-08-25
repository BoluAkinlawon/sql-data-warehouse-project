## Learn-by-doing Python ETL Pipeline

This project is a minimal, production-flavored ETL pipeline you can study and extend. It ingests a small synthetic orders dataset (CSV), transforms it with pandas, and loads the results to both SQLite and Parquet.

### What's inside
- Ingest: Generate/read CSV into a DataFrame
- Transform: Clean types, standardize text, compute metrics
- Load: Write to SQLite tables and Parquet files
- CLI: Orchestrate steps and run end-to-end

### Project layout
```
data-pipeline/
  data/
    raw/
    processed/
  src/
    pipeline/
      __init__.py
      config.py
      ingest.py
      transform.py
      load.py
      cli.py
  requirements.txt
  README.md
```

### Setup
```bash
cd data-pipeline
python -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Run the pipeline
Use the module runner and point `PYTHONPATH` at `src` so Python finds the `pipeline` package:
```bash
cd data-pipeline
PYTHONPATH=src python -m pipeline.cli run
```

You can also run individual steps:
```bash
PYTHONPATH=src python -m pipeline.cli ingest
PYTHONPATH=src python -m pipeline.cli transform
PYTHONPATH=src python -m pipeline.cli load
```

Outputs will be in `data/processed`:
- SQLite DB: `orders.sqlite` with tables `orders` and `revenue_by_state`
- Parquet: `orders_clean.parquet`
- CSV: `orders_clean.csv` and `revenue_by_state.csv`

### Learn
- Read `src/pipeline/*.py` to understand each step
- Add new transforms and targets (e.g., S3, Postgres)
- Schedule with cron or an orchestrator later (Airflow/Prefect)
