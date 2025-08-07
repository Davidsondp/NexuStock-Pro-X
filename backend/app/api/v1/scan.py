from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Product
from ..database import get_db

router = APIRouter()

@router.post("/process")
async def process_scanned_code(
    code: str,
    db: AsyncSession = Depends(get_db)
):
    # Buscar por código de barras
    product = await db.execute(
        select(Product).where(Product.barcode == code)
    )
    product = product.scalar()
    
    if not product:
        # Intentar buscar por ID si es un código QR personalizado
        product = await db.get(Product, code)
        if not product:
            raise HTTPException(404, "Producto no encontrado")
    
    return {
        "product": {
            "id": product.id,
            "name": product.name,
            "barcode": product.barcode,
            "price": product.price_htg
        },
        "currentStock": product.stock,
        "lastMovement": None  # Puede ampliarse
    }
