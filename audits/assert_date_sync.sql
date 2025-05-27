AUDIT (
  name assert_date_sync,
  blocking true,
);

--configuring an audit looks like this in the model config
-- audits (assert_date_sync(date_column:= event_date, upstream_ref:= sqlmesh_example.seed_model))
WITH current_max AS (
  SELECT max(@date_column) as max_date
  FROM @this_model
),
upstream_max AS (
  SELECT max(@date_column) as max_date 
  FROM @upstream_ref
)
SELECT *
FROM current_max, upstream_max
WHERE current_max.max_date < upstream_max.max_date


-- example audit log
/*
Executing SQL: SELECT COUNT(*) FROM (WITH "current_max"
       │  AS (SELECT MAX("event_date") AS "max_date" FROM (SELECT * FROM "db"."sqlmesh__sqlmesh_example"."sqlmesh_example__incremental_model__170
       │ 7007736" AS "sqlmesh_example__incremental_model__1707007736" WHERE "event_date" BETWEEN CAST('1970-01-01 00:00:00' AS TIMESTAMP) AND CAS
       │ T('1970-01-01 23:59:59.999999' AS TIMESTAMP)) AS "_q_0"), "upstream_max" AS (SELECT MAX("event_date") AS "max_date" FROM "db"."sqlmesh__
       │ sqlmesh_example"."sqlmesh_example__seed_model__203000760" AS "seed_model") SELECT * FROM "current_max" AS "current_max", "upstream_max" 
       │ AS "upstream_max" WHERE "current_max"."max_date" > "upstream_max"."max_date") AS "audit"

*/