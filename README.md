# DataLabs - Data Engineering Assessment

## Project Overview

This project demonstrates the implementation of two data pipelines in line with the requirements:

1. **Batch processing pipeline** using Apache Airflow and BigQuery for historical data ingestion and dimensional modeling in a data warehouse.
2. **Real-time streaming pipeline** using Kafka and MySQL to capture and process live transaction events.

The solution is built to cover the following objectives:

- Build end-to-end ETL/ELT pipelines
- Design a data warehouse model and architecture
- Explain data pipeline design decisions
- (Optional) Implement streaming data processing

---

## Data ETL (Batch Pipeline)

Built with **Apache Airflow** and **Google BigQuery**, this pipeline loads CSV sample data into staging tables and transforms them into a star schema data warehouse.

### Key Features

- Automated DAG scheduling for each dimensional and fact table
- CSV ingestion into staging layer (customers, products, transactions, etc.)
- Star schema transformations creating fact and dimension tables
- Partitioning and clustering on `fact_sales` for cost-optimized queries
- Reproducible local development with sample data

### Tables

**Staging**: `stg_customers`, `stg_products`, `stg_transactions`, `stg_transaction_items`, `stg_marketing_campaigns`

**Mart**: `dim_customer`, `dim_product`, `dim_campaign`, `dim_date`, `fact_sales`

See [data-etl/README.md](data-etl/README.md) for setup and details.

---

## Streaming Pipeline

A real-time transaction streaming architecture using **Apache Kafka** and **MySQL** to capture, process, and store live transaction events.

### Key Features

- Kafka producer that generates continuous transaction events
- Kafka consumer processing events in real-time
- MySQL backend for transaction storage
- Docker Compose setup for local development
- Automatic aggregations by minute for analytics

See [streaming-pipeline/README.md](streaming-pipeline/README.md) for setup and usage.

---

## Getting Started

Each pipeline has its own dedicated setup.

- **Batch ETL**: [data-etl/README.md](data-etl/README.md)
- **Streaming**: [streaming-pipeline/README.md](streaming-pipeline/README.md)