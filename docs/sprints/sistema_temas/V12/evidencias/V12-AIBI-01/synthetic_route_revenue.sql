WITH synthetic_routes AS (
  SELECT
    CAST(pickup_zip AS INT) AS pickup_zip,
    CAST(dropoff_zip AS INT) AS dropoff_zip,
    CAST(fare_amount AS DOUBLE) AS fare_amount
  FROM VALUES
    (10001, 10002, 14.50),
    (10001, 10002, 18.60),
    (10001, 10003, 13.75),
    (10001, 10003, 21.65),
    (10001, 10004, 16.20),
    (10001, 10005, 15.40),
    (10002, 10001, 15.95),
    (10002, 10003, 19.25),
    (10002, 10003, 22.85),
    (10002, 10004, 21.40),
    (10002, 10004, 26.90),
    (10002, 10005, 24.35),
    (10003, 10001, 23.80),
    (10003, 10002, 23.10),
    (10003, 10004, 22.70),
    (10003, 10004, 31.20),
    (10003, 10005, 25.10),
    (10003, 10005, 14.80),
    (10004, 10001, 27.30),
    (10004, 10002, 22.10),
    (10004, 10003, 29.40),
    (10004, 10005, 11.90),
    (10004, 10005, 15.30),
    (10005, 10001, 12.60),
    (10005, 10001, 16.75),
    (10005, 10002, 13.20),
    (10005, 10003, 12.95),
    (10005, 10004, 14.10)
  AS v(pickup_zip, dropoff_zip, fare_amount)
)
SELECT
  pickup_zip,
  dropoff_zip,
  concat(pickup_zip, '-', dropoff_zip) AS `Route`,
  count(*) AS `Number Trips`,
  sum(fare_amount) AS `Total Revenue`
FROM synthetic_routes
GROUP BY pickup_zip, dropoff_zip, concat(pickup_zip, '-', dropoff_zip)
ORDER BY pickup_zip ASC, dropoff_zip ASC
