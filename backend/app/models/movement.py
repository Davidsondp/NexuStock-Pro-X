from sqlalchemy import Column, String, Integer, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from .base import Base

class MovementType(PyEnum):
    ENTRADA = "entrada"
    SALIDA = "salida"
    AJUSTE = "ajuste"
    TRANSFERENCIA = "transferencia"

class InventoryMovement(Base):
    __tablename__ = "inventory_movements"

    id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    type = Column(Enum(MovementType), nullable=False)
    quantity = Column(Integer, nullable=False)
    reason = Column(String)
    reference = Column(String)  # Factura/Orden/Nota
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    location_from = Column(String)  # Para transferencias
    location_to = Column(String)    # Para transferencias
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def affect_stock(self):
        """Retorna el efecto neto en el inventario"""
        return self.quantity if self.type == MovementType.ENTRADA else -self.quantity
