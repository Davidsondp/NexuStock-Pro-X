import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from sqlalchemy import select, func

async def generar_reporte_ventas(
    db: AsyncSession,
    fecha_inicio: datetime,
    fecha_fin: datetime,
    categoria: str = None
):
    query = select(
        AnalisisVentas.fecha,
        func.sum(AnalisisVentas.ventas_totales).label("ventas_totales"),
        func.sum(AnalisisVentas.unidades_vendidas).label("unidades_vendidas")
    ).where(
        AnalisisVentas.fecha.between(fecha_inicio, fecha_fin)
    ).group_by(
        AnalisisVentas.fecha
    ).order_by(
        AnalisisVentas.fecha
    )
    
    if categoria:
        query = query.where(AnalisisVentas.categoria == categoria)
    
    resultado = await db.execute(query)
    return pd.DataFrame(resultado.all())

async def calcular_rotacion_inventario(
    db: AsyncSession,
    producto_id: str = None
):
    # Fórmula: (Ventas / Inventario Promedio)
    query = """
    SELECT 
        p.id,
        p.nombre->>'es' as nombre,
        COALESCE(SUM(CASE WHEN m.tipo = 'salida' THEN m.cantidad ELSE 0 END), 0) as unidades_vendidas,
        AVG(p.stock) as inventario_promedio,
        CASE 
            WHEN AVG(p.stock) > 0 
            THEN (SUM(CASE WHEN m.tipo = 'salida' THEN m.cantidad ELSE 0 END) / AVG(p.stock)) 
            ELSE 0 
        END as tasa_rotacion
    FROM productos p
    LEFT JOIN movimientos_inventario m ON p.id = m.producto_id
    GROUP BY p.id
    """
    
    if producto_id:
        query += f" HAVING p.id = '{producto_id}'"
    
    resultado = await db.execute(query)
    return pd.DataFrame(resultado.all())
