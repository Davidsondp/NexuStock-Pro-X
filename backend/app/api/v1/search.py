from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, and_
from ..models.product import Product
from ..database import get_db
from ..schemas.product import ProductResponse

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
async def search_products(
    query: str = Query(None, min_length=1),
    category: str = None,
    min_price: float = None,
    max_price: float = None,
    low_stock: bool = False,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Product).where(Product.is_active == True)
    
    if query:
        stmt = stmt.where(
            or_(
                Product.barcode.ilike(f"%{query}%"),
                Product.name["es"].astext.ilike(f"%{query}%"),
                Product.name["ht"].astext.ilike(f"%{query}%")
            )
        )
    
    if category:
        stmt = stmt.where(Product.category == category)
    
    if min_price is not None or max_price is not None:
        stmt = stmt.where(
            and_(
                Product.price_htg >= (min_price or 0),
                Product.price_htg <= (max_price or 999999)
            )
        )
    
    if low_stock:
        stmt = stmt.where(Product.stock <= Product.stock_min)
    
    result = await db.execute(stmt.order_by(Product.name["es"].astext))
    return result.scalars().all()
