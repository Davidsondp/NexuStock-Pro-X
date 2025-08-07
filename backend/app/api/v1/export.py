from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.product import Product
from ..database import get_db
import csv
import io

router = APIRouter()

@router.get("/products/csv")
async def export_products_csv(
    db: AsyncSession = Depends(get_db),
    _ = Depends(is_manager)
):
    result = await db.execute(select(Product).where(Product.is_active == True))
    products = result.scalars().all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Encabezados
    writer.writerow([
        "Código", "Nombre (ES)", "Nombre (HT)", "Precio HTG", 
        "Precio USD", "Stock", "Categoría"
    ])
    
    # Datos
    for p in products:
        writer.writerow([
            p.barcode,
            p.name.get("es", ""),
            p.name.get("ht", ""),
            str(p.price_htg),
            str(p.price_usd),
            str(p.stock),
            p.category
        ])
    
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=productos.csv"}
    )
