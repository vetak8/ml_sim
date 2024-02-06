SELECT DISTINCT
  day,
  wau
FROM (
  SELECT
    toDate(timestamp) AS day,
    count(DISTINCT user_id) OVER (ORDER BY day RANGE BETWEEN 6 PRECEDING AND CURRENT ROW) AS wau
  FROM
    default.churn_submits
)
ORDER BY
  day;
