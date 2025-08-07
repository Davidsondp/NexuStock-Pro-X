from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Product

async def process_barcode_scan(
    barcode: str, 
    quantity: int,
    movement_type: str,
    db: AsyncSession,
    user_id: str
):
    # Buscar producto por código de barras
    product = await db.execute(
        select(Product).where(Product.barcode == barcode)
    )
    product = product.scalar()
    
    if not product:
        return {"error": "Producto no encontrado"}
    
    # Validar stock para salidas
    if movement_type == "salida" and product.stock < quantity:
        return {"error": "Stock insuficiente"}
    
    # Retornar datos para confirmación
    return {
        "product": {
            "id": product.id,
            "name": product.localized_name(),
            "current_stock": product.stock,
            "new_stock": product.stock + (quantity if movement_type == "entrada" else -quantity)
        },
        "movement": {
            "type": movement_type,
            "quantity": quantity
        }
    }
