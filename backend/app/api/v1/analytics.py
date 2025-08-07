from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from ..services.analytics_service import (
    generate_sales_report,
    calculate_inventory_turnover
)
from ..database import get_db

router = APIRouter()

@router.get("/sales")
async def get_sales_analytics(
    start_date: datetime = Query(default_factory=lambda: datetime.now() - timedelta(days=30)),
    end_date: datetime = Query(default_factory=datetime.now),
    category: str = None,
    db: AsyncSession = Depends(get_db)
):
    report = await generate_sales_report(db, start_date, end_date, category)
    return report.to_dict("records")

@router.get("/inventory/turnover")
async def get_inventory_turnover(
    product_id: str = None,
    db: AsyncSession = Depends(get_db)
):
    turnover = await calculate_inventory_turnover(db, product_id)
    return turnover.to_dict("records")
