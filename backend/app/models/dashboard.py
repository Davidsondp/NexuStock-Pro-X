from sqlalchemy import Column, Integer, DateTime, Numeric
from sqlalchemy.sql import func
from .base import Base

class DashboardSnapshot(Base):
    __tablename__ = "dashboard_snapshots"
    
    id = Column(Integer, primary_key=True)
    total_products = Column(Integer)
    low_stock_items = Column(Integer)
    total_inventory_value_htg = Column(Numeric(12, 2))
    total_inventory_value_usd = Column(Numeric(12, 2))
    movements_today = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
