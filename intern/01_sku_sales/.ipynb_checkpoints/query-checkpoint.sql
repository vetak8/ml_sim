SELECT 
    toStartOfMonth(toDate(buy_date)) AS month,
    avg(check_amount) AS avg_check,
    arrayElement(quantilesExactExclusive(0.5)(check_amount), 1) AS median_check
FROM default.view_checks
GROUP BY month
ORDER BY month;
