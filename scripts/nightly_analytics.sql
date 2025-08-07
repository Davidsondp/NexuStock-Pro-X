-- Ejecutado diariamente vía cronjob
INSERT INTO sales_analytics
SELECT 
    gen_random_uuid(),
    p.id,
    date_trunc('day', m.created_at),
    SUM(p.price_htg * m.quantity),
    SUM(m.quantity),
    SUM((p.price_htg - p.cost) * m.quantity),
    p.category,
    NOW()
FROM inventory_movements m
JOIN products p ON m.product_id = p.id
WHERE m.type = 'salida'
  AND m.created_at >= date_trunc('day', NOW() - interval '1 day')
GROUP BY p.id, date_trunc('day', m.created_at), p.category;

-- Actualizar tendencias de inventario
INSERT INTO inventory_trends
SELECT 
    gen_random_uuid(),
    p.id,
    NOW(),
    p.stock,
    (SELECT forecast FROM ai_predictions WHERE product_id = p.id ORDER BY created_at DESC LIMIT 1),
    NOW()
FROM products p;
