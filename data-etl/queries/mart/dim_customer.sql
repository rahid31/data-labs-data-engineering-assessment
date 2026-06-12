CREATE OR REPLACE TABLE `{{project}}.{{mart_dataset}}.dim_customer`
PARTITION BY signup_date
CLUSTER BY customer_id, city
AS

SELECT DISTINCT
    customer_id,
    name,
    email,
    city,
    signup_date
FROM
`{{project}}.{{staging_dataset}}.stg_customers`;