SELECT 
    DATE(TO_CHAR(DATE_TRUNC('month', date), 'YYYY-MM-DD')) as time,
    mode,
    (COUNT(*) FILTER (WHERE status = 'Confirmed') * 100.0 / COUNT(*)) as percents
FROM new_payments
WHERE mode != 'Не определено'
GROUP BY time, mode
ORDER BY time, mode;
