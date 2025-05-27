MODEL (
  name sqlmesh_example.full_model,
  kind FULL,
  cron '@daily',
  grain item_id,
  -- audits (assert_positive_order_ids),
);

SELECT
  item_id,
  COUNT(DISTINCT id) AS num_orders,
  new_column,
  1 as new_column2,
  2 as new_column3,
  3 as new_column4,
FROM
  sqlmesh_example.incremental_model
GROUP BY item_id, new_column