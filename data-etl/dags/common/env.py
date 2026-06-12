import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    PROJECT_ID = os.getenv("BIGQUERY_PROJECT")
    DATASET_STAGING = os.getenv("BIGQUERY_DATASET_STAGING")
    DATASET_MART = os.getenv("BIGQUERY_DATASET_MART")
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    @staticmethod
    def table(dataset, table):
        return f"{Settings.PROJECT_ID}.{dataset}.{table}"