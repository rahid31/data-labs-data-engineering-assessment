CREATE OR REPLACE TABLE `{{project}}.{{mart_dataset}}.dim_campaign`
CLUSTER BY campaign_id, channel
AS

SELECT DISTINCT
    campaign_id,
    campaign_name,
    start_date,
    end_date,
    channel
FROM
`{{project}}.{{staging_dataset}}.stg_marketing_campaigns`;