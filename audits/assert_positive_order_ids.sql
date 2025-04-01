AUDIT (
  name assert_positive_order_ids,
  blocking false,
);

SELECT *
FROM @this_model
WHERE
  item_id < 0
  