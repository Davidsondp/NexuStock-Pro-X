from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey
from sqlalchemy.sql import func
from .base import Base

class SalesAnalytics(Base):
    __tablename__ = "sales_analytics"
    
    id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey("products.id"))
    date = Column(DateTime, nullable=False)
    total_sales = Column(Numeric(12, 2))
    units_sold = Column(Integer)
    profit = Column(Numeric(12, 2))
    category = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class InventoryTrend(Base):
    __tablename__ = "inventory_trends"
    
    id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey("products.id"))
    date = Column(DateTime, nullable=False)
    stock_level = Column(Integer)
    demand_forecast = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
