MODEL (
  name tcloud_demo.stg_orders,
  description 'This is a description of the stg_orders model',
  cron '@daily',
  grain order_id,
  tags (hello, world),
  audits (UNIQUE_VALUES(columns = (
      order_id
    )), NOT_NULL(columns = (
      order_id
  )))
);

SELECT
  id AS order_id, -- updates docs live with lsp jaiwoejfioawef
  user_id AS customer_id, -- comments are docs
  order_date, -- transaction order date
  status, -- order status
  1 as new_column
FROM tcloud_demo.seed_raw_orders