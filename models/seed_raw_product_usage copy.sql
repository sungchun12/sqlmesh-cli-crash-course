MODEL (
  name sqlmesh_example.raw_product_usage,
  kind SEED (
    path '../seeds/raw_product_usage.csv'
  ),
  columns (
    product_id STRING,
    customer_id STRING,
    last_usage_date TIMESTAMP,
    usage_count INTEGER,
    feature_utilization_score FLOAT,
    user_segment STRING
  ),
  grain (product_id, customer_id)
);
