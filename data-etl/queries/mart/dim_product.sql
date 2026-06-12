CREATE OR REPLACE TABLE `{{project}}.{{mart_dataset}}.dim_product`
CLUSTER BY product_id, category
AS

SELECT DISTINCT
    product_id,
    product_name,
    category,
    price
FROM
`{{project}}.{{staging_dataset}}.stg_products`;