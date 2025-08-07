from sqlalchemy import Column, String, Integer, Numeric, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from .base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True)
    barcode = Column(String, unique=True, index=True)
    name = Column(JSON)  # {"es": "Nombre", "ht": "Non", "en": "Name"}
    description = Column(JSON)
    price_htg = Column(Numeric(12, 2))
    price_usd = Column(Numeric(12, 2))
    price_eur = Column(Numeric(12, 2))
    cost = Column(Numeric(12, 2))
    stock = Column(Integer, default=0)
    stock_min = Column(Integer, default=5)
    category = Column(String)
    supplier_id = Column(String, ForeignKey("suppliers.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    def localized_name(self, lang: str = "es"):
        return self.name.get(lang, self.name["es"])

    def current_price(self, currency: str = "htg"):
        return getattr(self, f"price_{currency.lower()}")
