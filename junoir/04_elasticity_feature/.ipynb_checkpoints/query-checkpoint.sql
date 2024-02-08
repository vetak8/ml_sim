SELECT
  sku,
  dates,
  avg(price) AS price,
  count(user) AS qty
FROM
  transactions
GROUP BY
  sku,
  dates