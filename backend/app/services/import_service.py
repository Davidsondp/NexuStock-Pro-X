from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.product import Product
import csv
import io

async def import_products_from_csv(
    file: UploadFile, 
    db: AsyncSession,
    user_id: str
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, "Solo se permiten archivos CSV")
    
    contents = await file.read()
    csv_data = io.StringIO(contents.decode('utf-8'))
    reader = csv.DictReader(csv_data)
    
    products = []
    errors = []
    
    for row in reader:
        try:
            product_data = {
                "barcode": row["barcode"],
                "name": {
                    "es": row["nombre_es"],
                    "ht": row["nombre_ht"],
                    "en": row["nombre_en"]
                },
                "price_htg": float(row["precio_htg"]),
                "stock": int(row["stock"]),
                "category": row["categoria"]
            }
            products.append(product_data)
        except Exception as e:
            errors.append(f"Error en línea {reader.line_num}: {str(e)}")
    
    # Guardar en lote
    for product in products:
        db.add(Product(**product, created_by=user_id))
    
    await db.commit()
    return {
        "imported": len(products),
        "errors": errors
    }
