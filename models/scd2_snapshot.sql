MODEL (
  name tcloud_demo.scd2_snapshot,
  kind SCD_TYPE_2_BY_TIME (
    unique_key id,
    updated_at_name order_date
  ),
  grain (id, user_id)
);

SELECT
    id,
    user_id,
    order_date,
    status,
    1 as new_column
FROM
  tcloud_demo.seed_raw_orders
