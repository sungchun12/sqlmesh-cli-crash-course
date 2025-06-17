MODEL (
  name sqlmesh_example.incremental_model,
  kind INCREMENTAL_BY_TIME_RANGE (
    time_column event_date
  ),
  description "awuioehfoiah2uwhoiahwoidfvcoawefjoiajwoiefoia wefjaiowefjoiajsiodfoiajwioefoiawjoiefawef",
  start '2020-01-01',
  cron '@daily',
  grain (id, event_date),
  audits (assert_date_sync(date_column:= event_date, upstream_ref:= sqlmesh_example.seed_model))
);

SELECT
  id,
  item_id,
  event_date,
  28 as new_column,
  1 as new_column2,
  2 as new_column3,
  3 as new_column4,
  5 as new_column5,
  8 as new_column1,
  2 as new_column6,
FROM
  sqlmesh_example.seed_model
WHERE
  event_date BETWEEN @start_date AND @end_date
  