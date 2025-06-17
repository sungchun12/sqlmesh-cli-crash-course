MODEL (
  name sqlmesh_example.seed_model,
  kind SEED (
    path '../seeds/seed_data.csv'
  ),
  columns (
    id INTEGER,
    item_id FLOAT,
    event_date DATE
  ),
  grain (id, event_date)
);
