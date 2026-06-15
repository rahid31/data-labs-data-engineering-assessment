CREATE OR REPLACE TABLE `{{project}}.{{mart_dataset}}.fact_sales`
PARTITION BY DATE(transaction_date)
CLUSTER BY product_id, customer_id, transaction_id
AS

SELECT
    b.transaction_item_id,
    a.transaction_id,
    a.customer_id,
    b.product_id,
    a.transaction_date,
    b.quantity,
    b.price,
    b.quantity * b.price AS sales_amount
FROM
`{{project}}.{{staging_dataset}}.stg_transactions` a
JOIN
`{{project}}.{{staging_dataset}}.stg_transaction_items` b ON a.transaction_id = b.transaction_id;