MODEL (
  name demo.incrementals_demo,
  kind INCREMENTAL_BY_TIME_RANGE (
    -- How does this model kind behave?
    --   DELETE by time range, then INSERT
    time_column transaction_date,

    -- How do I handle late-arriving data?
    --   Handle late-arriving events for the past 2 (2*1) days based on cron
    --   interval. Each time it runs, it will process today, yesterday, and
    --   the day before yesterday.
    lookback 2,
  ),

  -- Don't backfill data before this date
  start '2024-10-25',

  -- What schedule should I run these at?
  --   Daily at Midnight UTC
  cron '@daily',

  -- Good documentation for the primary key
  grain transaction_id,

  -- How do I test this data?
  --   Validate that the `transaction_id` primary key values are both unique
  --   and non-null. Data audit tests only run for the processed intervals,
  --   not for the entire table.
  audits (
    UNIQUE_VALUES(columns = (transaction_id)),
    NOT_NULL(columns = (transaction_id))
  )
);

WITH sales_data AS (
  SELECT
    transaction_id,
    product_id,
    customer_id,
    transaction_amount,
    -- How do I account for UTC vs. PST (California baby) timestamps?
    --   Make sure all time columns are in UTC and convert them to PST in the
    --   presentation layer downstream.
    transaction_timestamp,
    payment_method,
    currency
  FROM sqlmesh_example.raw_sales  -- Source A: sales data
  -- How do I make this run fast and only process the necessary intervals?
  --   Use our date macros that will automatically run the necessary intervals.
  --   Because SQLMesh manages state, it will know what needs to run each time
  --   you invoke `sqlmesh run`.
  WHERE transaction_timestamp BETWEEN @start_dt AND @end_dt
),

product_usage AS (
  SELECT
    product_id,
    customer_id,
    last_usage_date,
    usage_count,
    feature_utilization_score,
    user_segment
  FROM sqlmesh_example.raw_product_usage  -- Source B
  -- Include usage data from the 30 days before the interval
  WHERE last_usage_date BETWEEN @start_dt - INTERVAL '30 DAYS' AND @end_dt
)

SELECT
  s.transaction_id,
  s.product_id,
  s.customer_id,
  s.transaction_amount,
  -- Extract the date from the timestamp to partition by day
  DATE(s.transaction_timestamp) as transaction_date,
  -- Convert timestamp to PST using a SQL function in the presentation layer for end users
  DATETIME(s.transaction_timestamp, 'America/Los_Angeles') as transaction_timestamp_pst,
  s.payment_method,
  s.currency,
  -- Product usage metrics
  p.last_usage_date,
  p.usage_count,
  p.feature_utilization_score,
  p.user_segment,
  -- Derived metrics
  CASE
    WHEN p.usage_count > 100 AND p.feature_utilization_score > 0.8 THEN 'Power User'
    WHEN p.usage_count > 50 THEN 'Regular User'
    WHEN p.usage_count IS NULL THEN 'New User'
    ELSE 'Light User'
  END as user_type,
  -- Time since last usage
  DATE_DIFF('day',s.transaction_timestamp, p.last_usage_date) as days_since_last_usage
FROM sales_data s
LEFT JOIN product_usage p
  ON s.product_id = p.product_id
  AND s.customer_id = p.customer_id
