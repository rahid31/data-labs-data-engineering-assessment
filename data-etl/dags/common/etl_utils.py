import logging
import pandas as pd
from pathlib import Path

from google.cloud import bigquery
from google.oauth2 import service_account

from common.env import Settings

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def get_client():

    credentials = (
        service_account.Credentials
        .from_service_account_file(
            Settings.GOOGLE_APPLICATION_CREDENTIALS
        )
    )

    return bigquery.Client(
        project=Settings.PROJECT_ID,
        credentials=credentials
    )


def build_job_config(config):

    job_cfg = config.get("job_config", {})

    schema = [
        bigquery.SchemaField(
            field["name"],
            field["type"]
        )
        for field in job_cfg.get("schema", [])
    ]

    cfg = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition=job_cfg.get(
            "write_disposition",
            "WRITE_TRUNCATE"
        )
    )

    # optional partition
    partition = job_cfg.get("partition")

    if partition:

        cfg.time_partitioning = (
            bigquery.TimePartitioning(
                type_=bigquery.TimePartitioningType.DAY,
                field=partition["field"]
            )
        )

    # optional clustering
    cluster = job_cfg.get("cluster")

    if cluster:
        cfg.clustering_fields = cluster

    return cfg

def ingest_csv(table_name, config):

    client = get_client()

    csv_file = (
        PROJECT_ROOT
        / "sample_data"
        / config["file"]
    )

    # Extract date and timestamp columns from schema
    job_cfg = config.get("job_config", {})
    schema = job_cfg.get("schema", [])
    
    date_cols = [
        field["name"] 
        for field in schema 
        if field["type"] in ["DATE", "TIMESTAMP", "DATETIME"]
    ]

    # Read CSV with date handling
    df = pd.read_csv(csv_file)

    for field in schema:

        col = field["name"]

        if col not in df.columns:
            continue

        if field["type"] == "DATE":

            df[col] = pd.to_datetime(
                df[col],
                errors="coerce"
            ).dt.date

        elif field["type"] == "TIMESTAMP":

            df[col] = pd.to_datetime(
                df[col],
                utc=True,
                errors="coerce"
            ).dt.tz_localize(None)

    table_id = Settings.table(
        Settings.DATASET_STAGING,
        config["table"]
    )

    if df.empty:
        logger.warning(f"No data to load for {table_id}")
        return

    job = client.load_table_from_dataframe(
        df,
        table_id,
        job_config=build_job_config(config)
    )

    job.result()
    print(f"Loaded {job.output_rows} rows into {table_id}.")

def run_sql(sql_path):

    client = get_client()

    sql_file = PROJECT_ROOT / sql_path

    if not sql_file.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_file}")

    sql = sql_file.read_text()

    sql = sql.replace("{{project}}", Settings.PROJECT_ID)
    sql = sql.replace("{{staging_dataset}}", Settings.DATASET_STAGING)
    sql = sql.replace("{{mart_dataset}}", Settings.DATASET_MART)

    client.query(sql).result()

    print(f"Executed SQL from {sql_path}")