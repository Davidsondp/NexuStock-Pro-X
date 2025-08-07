from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from datetime import datetime, timedelta
from ..models import Product, InventoryMovement, DashboardSnapshot

async def generate_dashboard_data(db: AsyncSession):
    # Productos totales y en bajo stock
    total_products = await db.scalar(
        select(func.count(Product.id)).where(Product.is_active == True)
    )
    
    low_stock = await db.scalar(
        select(func.count(Product.id)).where(
            and_(
                Product.is_active == True,
                Product.stock <= Product.stock_min
            )
        )
    )
    
    # Valor total del inventario
    inventory_value = await db.scalar(
        select(func.sum(Product.price_htg * Product.stock)).where(
            Product.is_active == True
        )
    )
    
    # Movimientos hoy
    today = datetime.now().date()
    movements_today = await db.scalar(
        select(func.count(InventoryMovement.id)).where(
            func.date(InventoryMovement.created_at) == today
        )
    )
    
    # Guardar snapshot
    snapshot = DashboardSnapshot(
        total_products=total_products,
        low_stock_items=low_stock,
        total_inventory_value_htg=inventory_value or 0,
        movements_today=movements_today
    )
    db.add(snapshot)
    await db.commit()
    
    return snapshot
