SELECT vendor , COUNT(DISTINCT brand) AS brand
FROM sku_dict_another_one
where  brand is not null
GROUP BY vendor
ORDER BY brand DESC
LIMIT 10;