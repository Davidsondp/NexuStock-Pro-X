from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Optional
from ..database import get_db
from ..services.export_service import export_products_to_csv, export_movements_to_excel
from ..utils.security import is_manager

router = APIRouter()

@router.get("/products/csv")
async def export_products_csv(
    low_stock: Optional[bool] = Query(None),
    category: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    _ = Depends(is_manager)
):
    filters = {}
    if low_stock:
        filters["low_stock"] = True
    if category:
        filters["category"] = category
    
    return await export_products_to_csv(db, filters)

@router.get("/movements/excel")
async def export_movements_excel(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    type: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    _ = Depends(is_manager)
):
    filters = {}
    if start_date:
        filters["start_date"] = start_date
    if end_date:
        filters["end_date"] = end_date
    if type:
        filters["type"] = type
    
    return await export_movements_to_excel(db, filters)
