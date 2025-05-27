MODEL (
  name tcloud_demo.stg_orders,
  cron '@daily',
  grain order_id,
  audits (UNIQUE_VALUES(columns = (
      order_id
    )), NOT_NULL(columns = (
      order_id
  )))
);

SELECT
  id AS order_id,
  user_id AS customer_id, --aiwenfionaoiwjsfe
  order_date, -- transaction order date
  status -- this is a comment
FROM tcloud_demo.seed_raw_orders