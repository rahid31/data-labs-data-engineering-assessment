# Architecture Overview

This project implements a simple and scalable ELT pipeline using Apache Airflow and Google BigQuery. The design follows a configuration-driven approach where YAML files define tables, schemas, and transformation logic, enabling new datasets to be added with minimal code changes.

---

## Architecture Flow

```text
CSV Files
   |
   v
Airflow DAG (dynamic per table from YAML)
   |
   v
ingest_csv task
   - Read CSV from local storage
   - Load into BigQuery staging tables (WRITE_TRUNCATE)
   |
   v
BigQuery Staging Layer
   - stg_customers
   - stg_products
   - stg_transactions
   - stg_transaction_items
   - stg_marketing_campaigns
   |
   v
run_sql task
   - Execute SQL from /queries/mart
   - Build dimensional model (star schema)
   |
   v
BigQuery Mart Layer
   - fact_sales
   - dim_customer
   - dim_product
   - dim_date
   - dim_campaign
```

## Dags Design
Design

Staging tables are a direct copy of CSV data into BigQuery. This keeps ingestion simple and repeatable.

The mart layer is built using SQL inside BigQuery to form a basic star schema. Fact table is built from transactions and transaction items, while dimensions are built from their respective staging tables.

Everything is driven by YAML config:

- table list
- schema
- partition & clustering
- file mapping

So adding a new dataset is just:

- add CSV
- update YAML
- add SQL (if transformation needed)

---

## Data Warehouse Design

A star schema was selected to support analytical workloads and simplify reporting queries.

## ERD

![Star Schema ERD](docs/bq_warehouse_erd.png)

### Fact Table

`fact_sales` stores transaction-level sales metrics and represents the central business process of the model.

Grain:

* One row per transaction item.

Measures:

* quantity
* price
* sales_amount
* total_amount

### Dimension Tables

#### dim_customer

Contains customer attributes used for segmentation and customer analysis.

#### dim_product

Contains product attributes used for category and product performance reporting.

#### dim_date

Provides a standard calendar dimension to support time-based aggregations.

#### dim_campaign

Contains marketing campaign metadata. The source data does not include a relationship between campaigns and transactions; therefore, this dimension is modeled independently and is not currently joined to the sales fact table.

### Partitioning and Clustering

The largest table, `fact_sales`, is partitioned by transaction date and clustered by customer_id and product_id to optimize analytical queries and reduce scan costs.

`stg_transactions` is partitioned by transaction_date and clustered by customer_id to improve transformation performance.

Dimension tables remain unpartitioned because of their relatively small size, with clustering applied where beneficial for join performance.

### Loading Strategy

CSV files are ingested into staging tables using full refresh (`WRITE_TRUNCATE`). Transformation jobs create and maintain dimensional tables and fact tables using SQL executed through Apache Airflow.

This approach provides a reproducible local development workflow while remaining compatible with production BigQuery deployment patterns.
