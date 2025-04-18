MODEL (
  name sqlmesh_example.view_model,
  kind VIEW,
  cron '@daily',
  grain item_id,
  audits (UNIQUE_VALUES(columns = (
      item_id
    )), NOT_NULL(columns = (
      item_id
  )),
  assert_positive_order_ids)
);

SELECT
  item_id,
  COUNT(DISTINCT id) AS num_orders,
FROM
  sqlmesh_example.incremental_model
GROUP BY item_id
  