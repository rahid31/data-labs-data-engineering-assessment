import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from common.config_bq import load_bq_config
from common.etl_utils import ingest_csv, run_sql

logger = logging.getLogger(__name__)


cfg = load_bq_config()

DEFAULT_ARGS = {
    "owner": "airflow"
}

def create_staging_dag(name, conf):

    dag = DAG(
        dag_id=f"etl_{conf['table']}",
        start_date=datetime(2026, 1, 1),
        catchup=False,
        schedule=None,
        default_args=DEFAULT_ARGS,
        tags=["staging"]
    )

    PythonOperator(
        task_id="ingest_csv",
        python_callable=ingest_csv,
        op_kwargs={
            "table_name": name,
            "config": conf
        },
        dag=dag
    )

    return dag

def create_mart_dag(name, conf):

    dag = DAG(
        dag_id=f"etl_{name}",
        start_date=datetime(2026, 1, 1),
        catchup=False,
        schedule=None,
        default_args=DEFAULT_ARGS,
        tags=["mart"]
    )

    PythonOperator(
        task_id="run_sql",
        python_callable=run_sql,
        op_kwargs={
            "sql_path": conf["sql"]
        },
        dag=dag
    )

    return dag

for table_name, conf in cfg["staging"].items():

    globals()[
        f"etl_{conf['table']}"
    ] = create_staging_dag(
        table_name,
        conf
    )


for mart_name, conf in cfg.get("mart", {}).items():

    try:
        dag = create_mart_dag(
            mart_name,
            conf
        )

        if dag:
            globals()[dag.dag_id] = dag

    except Exception as e:
        logger.exception(
            f"Failed to create DAG for {mart_name}: {e}"
        )