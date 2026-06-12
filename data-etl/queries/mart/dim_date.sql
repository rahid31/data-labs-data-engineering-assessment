CREATE OR REPLACE TABLE `{{project}}.{{mart_dataset}}.dim_date`
CLUSTER BY date_key
AS

SELECT DISTINCT

    CAST(
        FORMAT_DATE(
            '%Y%m%d',
            DATE(transaction_date)
        ) AS INT64
    ) AS date_key,

    DATE(transaction_date) AS full_date,

    EXTRACT(YEAR FROM transaction_date) AS year,

    EXTRACT(QUARTER FROM transaction_date) AS quarter,

    EXTRACT(MONTH FROM transaction_date) AS month,

    EXTRACT(DAY FROM transaction_date) AS day,

    EXTRACT(DAYOFWEEK FROM transaction_date) AS day_of_week

FROM
`{{project}}.{{staging_dataset}}.stg_transactions`;