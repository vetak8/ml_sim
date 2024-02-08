SELECT 
    DATE(TO_CHAR(DATE_TRUNC('month', date), 'YYYY-MM-DD')) AS time,
    SUM(amount) / COUNT(DISTINCT email_id) AS arppu,
    SUM(amount) / COUNT(*) AS aov
FROM 
    new_payments
WHERE 
    status = 'Confirmed'
GROUP BY 
    time
ORDER BY 
    time;
