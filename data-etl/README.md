# Data ETL - Airflow + BigQuery

A simple ETL pipeline built with Apache Airflow and Google BigQuery.

The pipeline loads CSV files into BigQuery staging tables and transforms them into dimensional and fact tables using SQL-based transformations.

## Overview

### Staging Layer

CSV files are loaded into BigQuery staging tables:

* `stg_customers`
* `stg_products`
* `stg_transactions`
* `stg_transaction_items`
* `stg_marketing_campaigns`

### Mart Layer

Transformations create the following warehouse tables:

* `dim_customer`
* `dim_product`
* `dim_campaign`
* `dim_date`
* `fact_sales`

Each table is managed through its own Airflow DAG for easier monitoring and troubleshooting.

---

# Project Structure

```text
data_etl/
├── .venv 
├── airflow/
│   ├── airflow.db
│   ├── airflow.cfg
│   ├── logs/
├── config/
│   └── bq_config.yaml
├── credentials/
│   ├── service-account.json
├── dags/
│   ├── main.py
│   └── common/
│       ├── __init__.py
│       ├── env.py
│       ├── config_bq.py
│       └── etl_utils.py
├── queries/
│   └── mart/
│       ├── dim_customer.sql
│       ├── dim_product.sql
│       ├── dim_campaign.sql
│       ├── dim_date.sql
│       └── fact_sales.sql
├── sample_data/
│   ├── customers.csv
│   ├── products.csv
│   ├── transactions.csv
│   ├── transaction_items.csv
│   └── marketing_campaigns.csv
├── .env
├── .gitignore
├── DESIGN.md
├── README.md
└── requirements.txt
```

---

# Apache Airflow Setup

## Create and Activate Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

## Install Dependencies

Download Airflow constraints:

```bash
curl -o constraints-3.12.txt \
https://raw.githubusercontent.com/apache/airflow/constraints-3.1.8/constraints-3.12.txt
```

Install project requirements:

```bash
pip install -r requirements.txt \
  --constraint constraints-3.12.txt
```

## Configure Airflow Home

```bash
mkdir airflow
export AIRFLOW_HOME=$(pwd)/airflow
```

## Configure Airflow Dags Core Folder

1. Go to airflow folder
2. Open airflow.cfg
3. Change this line:

```text
dags_folder = {your dags folder path}
```

## Disable Example DAGs (Optional)

Update `airflow.cfg`:

```ini
[core]
load_examples = False
```

## Initialize Airflow

```bash
airflow db migrate
```

## Start Airflow

Terminal:

```bash
airflow standalone
```

Or

Terminal 1:

```bash
airflow scheduler
```

Terminal 2:

```bash
airflow api-server
```

Access Airflow UI:

```text
http://localhost:8080
```

Verify DAG loading:

```bash
airflow dags list
```

Check import errors:

```bash
airflow dags list-import-errors
```

## Additional: Account Credentials

Starting airflow with `airflow standalone` command will automatically generate credentials json file:
```text
{your airflow folder}/simple_auth_manager_passwords.json.generated
```

---

# BigQuery Setup

## Create Service Account

1. Open Google Cloud Console.
2. Navigate to:

```text
IAM & Admin → Service Accounts
```

3. Create a new service account.
4. Assign required BigQuery roles.

Recommended roles:

* BigQuery Job User
* BigQuery Data Editor

For local testing, BigQuery Admin is acceptable.

## Generate JSON Key

1. Open the service account.
2. Go to:

```text
Keys → Add Key → Create New Key
```

3. Select:

```text
JSON
```

4. Download the generated key.

Store the file locally:

```text
data_etl/credentials/service-account.json
```

Never commit credentials to source control.

Example `.gitignore`:

```gitignore
credentials/
.env
```

---

# Environment Configuration

Create a `.env` file in the project root.

Example:

```env
BIGQUERY_PROJECT=my-gcp-project
BIGQUERY_DATASET_STAGING=staging
BIGQUERY_DATASET_MART=mart

GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/data_etl/credentials/service-account.json
```

Use absolute paths whenever possible.

---

# Configuration

Table definitions are maintained in:

```text
config/bq_config.yaml
```

The configuration contains:

* Source CSV file
* Target staging table
* Column schema
* Partition configuration
* Clustering configuration
* Transformation SQL definitions

To add a new source table:

1. Add a CSV file to `sample_data/`
2. Add table configuration to `config/bq_config.yaml`
3. Add transformation SQL to `queries/mart/` if required

No DAG code changes are required.

---

# DAGs

## Staging DAGs

```text
etl_stg_customers
etl_stg_products
etl_stg_transactions
etl_stg_transaction_items
etl_stg_marketing_campaigns
```

## Mart DAGs

```text
etl_dim_customer
etl_dim_product
etl_dim_campaign
etl_dim_date
etl_fact_sales
```

# SQL Templates

Transformation SQL files support variable substitution.

Available variables:

```sql
{{project}}
{{staging_dataset}}
{{mart_dataset}}
```

Example:

```sql
CREATE OR REPLACE TABLE `{{project}}.{{mart_dataset}}.dim_customer`
AS

SELECT *
FROM `{{project}}.{{staging_dataset}}.stg_customers`;
```

---

# Notes

* Staging loads use `WRITE_TRUNCATE`
* Incremental loading is not implemented
* Tables are recreated on each execution
* Intended for local development and assessment use cases
* BigQuery datasets must exist before execution
* Airflow DAGs are generated dynamically from YAML configuration
