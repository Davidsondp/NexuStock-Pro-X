from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import csv
import io
from ..models.product import Product
from ..schemas.product import ProductCreate, ProductUpdate, ProductResponse
from ..database import get_db
from ..utils.security import is_admin, is_manager

router = APIRouter()

@router.post("/", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db),
    _ = Depends(is_admin)
):
    # Verificar si el código de barras ya existe
    existing = await db.execute(
        select(Product).where(Product.barcode == product.barcode)
    )
    if existing.scalar():
        raise HTTPException(400, "El código de barras ya existe")
    
    db_product = Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

@router.get("/{product_id}", response_model=ProductResponse)
async def read_product(
    product_id: str,
    db: AsyncSession = Depends(get_db),
    _ = Depends(is_manager)
):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Producto no encontrado")
    return product

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    _ = Depends(is_admin)
):
    db_product = await db.get(Product, product_id)
    if not db_product:
        raise HTTPException(404, "Producto no encontrado")
    
    for field, value in product.dict(exclude_unset=True).items():
        setattr(db_product, field, value)
    
    await db.commit()
    await db.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    db: AsyncSession = Depends(get_db),
    _ = Depends(is_admin)
):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Producto no encontrado")
    
    # Eliminación lógica
    product.is_active = False
    await db.commit()
    return {"message": "Producto desactivado"}
