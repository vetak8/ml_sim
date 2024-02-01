SELECT toDate(timestamp) AS day, COUNT(DISTINCT user_id) AS dau
FROM default.churn_submits
GROUP BY day
ORDER BY day;
