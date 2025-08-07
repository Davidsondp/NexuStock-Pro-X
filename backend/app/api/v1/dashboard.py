from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..services.dashboard_service import generate_dashboard_data
from ..models import DashboardSnapshot
from ..database import get_db
from ..schemas.dashboard import DashboardResponse, MovementTrend
from ..utils.security import is_manager

router = APIRouter()

@router.get("/", response_model=DashboardResponse)
async def get_dashboard_data(
    db: AsyncSession = Depends(get_db),
    _ = Depends(is_manager)
):
    return await generate_dashboard_data(db)
@router.get("/category-distribution")
async def get_category_distribution(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(
            Product.category,
            func.count(Product.id).label("count")
        )
        .where(Product.is_active == True)
        .group_by(Product.category)
    )

@router.get("/movement-trends", response_model=List[MovementTrend])
async def get_movement_trends(
    days: int = 30,
    db: AsyncSession = Depends(get_db)
):
    date_threshold = datetime.now() - timedelta(days=days)
    
    result = await db.execute(
        select(
            func.date(InventoryMovement.created_at).label("date"),
            InventoryMovement.type,
            func.sum(InventoryMovement.quantity).label("total")
        )
        .where(InventoryMovement.created_at >= date_threshold)
        .group_by("date", "type")
        .order_by("date")
    )
    
    return result.all()
