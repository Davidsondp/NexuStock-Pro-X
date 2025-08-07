import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from sqlalchemy import select, func

async def generate_sales_report(
    db: AsyncSession,
    start_date: datetime,
    end_date: datetime,
    category: str = None
):
    query = select(
        SalesAnalytics.date,
        func.sum(SalesAnalytics.total_sales).label("total_sales"),
        func.sum(SalesAnalytics.units_sold).label("units_sold")
    ).where(
        SalesAnalytics.date.between(start_date, end_date)
    ).group_by(
        SalesAnalytics.date
    ).order_by(
        SalesAnalytics.date
    )
    
    if category:
        query = query.where(SalesAnalytics.category == category)
    
    result = await db.execute(query)
    return pd.DataFrame(result.all())

async def calculate_inventory_turnover(
    db: AsyncSession,
    product_id: str = None
):
    # Fórmula: Costo de Ventas / Inventario Promedio
    query = """
    SELECT 
        p.id,
        p.name->>'es' as name,
        COALESCE(SUM(CASE WHEN m.type = 'salida' THEN m.quantity ELSE 0 END), 0) as units_sold,
        AVG(p.stock) as avg_stock,
        CASE 
            WHEN AVG(p.stock) > 0 
            THEN (SUM(CASE WHEN m.type = 'salida' THEN m.quantity ELSE 0 END) / AVG(p.stock)) 
            ELSE 0 
        END as turnover_rate
    FROM products p
    LEFT JOIN inventory_movements m ON p.id = m.product_id
    GROUP BY p.id
    """
    
    if product_id:
        query += f" HAVING p.id = '{product_id}'"
    
    result = await db.execute(query)
    return pd.DataFrame(result.all())
