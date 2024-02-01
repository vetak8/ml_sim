SELECT vendor, COUNT(sku_type) AS sku
FROM sku_dict_another_one
where vendor is not null
GROUP BY vendor
ORDER BY sku DESC
LIMIT 10;