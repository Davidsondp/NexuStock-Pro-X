from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..models import InventoryMovement, Product
from ..schemas.movement import MovementCreate, MovementResponse
from ..database import get_db
from ..utils.security import is_manager
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/", response_model=MovementResponse)
async def create_movement(
    movement: MovementCreate,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(is_manager)
):
    # Verificar producto
    product = await db.get(Product, movement.product_id)
    if not product:
        raise HTTPException(404, "Producto no encontrado")
    
    # Validar stock para salidas
    if movement.type == "salida" and product.stock < movement.quantity:
        raise HTTPException(400, "Stock insuficiente")
    
    # Crear movimiento
    db_movement = InventoryMovement(
        **movement.dict(),
        user_id=user_id
    )
    db.add(db_movement)
    
    # Actualizar stock
    if movement.type == "entrada":
        product.stock += movement.quantity
    else:
        product.stock -= movement.quantity
    
    await db.commit()
    await db.refresh(db_movement)
    return db_movement

@router.get("/", response_model=List[MovementResponse])
async def list_movements(
    product_id: str = None,
    type: str = None,
    start_date: datetime = None,
    end_date: datetime = None,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    query = select(InventoryMovement).order_by(InventoryMovement.created_at.desc())
    
    if product_id:
        query = query.where(InventoryMovement.product_id == product_id)
    
    if type:
        query = query.where(InventoryMovement.type == type)
    
    if start_date:
        query = query.where(InventoryMovement.created_at >= start_date)
    
    if end_date:
        query = query.where(InventoryMovement.created_at <= end_date)
    
    if limit:
        query = query.limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()
