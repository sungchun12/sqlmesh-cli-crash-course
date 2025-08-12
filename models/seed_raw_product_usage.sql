MODEL (
  name sqlmesh_example.raw_sales,
  kind SEED (
    path '../seeds/raw_sales.csv'
  ),
  columns (
    transaction_id STRING,
    product_id STRING,
    customer_id STRING,
    transaction_amount FLOAT,
    transaction_timestamp TIMESTAMP,
    payment_method STRING,
    currency STRING
  ),
  grain (product_id, customer_id)
);
