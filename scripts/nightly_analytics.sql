-- Ejecutado diariamente vía cronjob
INSERT INTO analisis_ventas
SELECT 
    gen_random_uuid(),
    p.id,
    date_trunc('day', m.creado_en),
    SUM(p.precio_htg * m.cantidad),
    SUM(m.cantidad),
    SUM((p.precio_htg - p.costo) * m.cantidad),
    p.categoria,
    NOW()
FROM movimientos_inventario m
JOIN productos p ON m.producto_id = p.id
WHERE m.tipo = 'salida'
  AND m.creado_en >= date_trunc('day', NOW() - interval '1 day')
GROUP BY p.id, date_trunc('day', m.creado_en), p.categoria;

-- Actualizar tendencias de inventario
INSERT INTO tendencias_inventario
SELECT 
    gen_random_uuid(),
    p.id,
    NOW(),
    p.stock,
    (SELECT pronostico FROM predicciones_ia WHERE producto_id = p.id ORDER BY creado_en DESC LIMIT 1),
    NOW()
FROM productos p;
