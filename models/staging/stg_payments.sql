MODEL (
  name tcloud_demo.stg_payments,
  cron '@daily',
  grains payment_id,
  audits (UNIQUE_VALUES(columns = (
      payment_id
    )), NOT_NULL(columns = (
      payment_id
  )))
);

SELECT
  id AS payment_id,
  order_id,
  payment_method, -- credit card, cash
  'advanced_cll_column' AS advanced_cll_column, /* Tobiko Cloud only feature  */
  amount / 100 AS amount, /* `amount` is currently stored in cents, so we convert it to dollars */
  '1255' AS new_column_demos, /* non-breaking change example  */
  1 as new_column
FROM tcloud_demo.seed_raw_payments