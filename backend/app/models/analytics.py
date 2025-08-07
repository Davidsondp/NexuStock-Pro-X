from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey, Integer
from sqlalchemy.sql import func
from .base import Base

class AnalisisVentas(Base):
    __tablename__ = "analisis_ventas"
    
    id = Column(String, primary_key=True)
    producto_id = Column(String, ForeignKey("productos.id"))
    fecha = Column(DateTime, nullable=False)
    ventas_totales = Column(Numeric(12, 2))  # En HTG
    unidades_vendidas = Column(Integer)
    ganancia = Column(Numeric(12, 2))
    categoria = Column(String)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

class TendenciaInventario(Base):
    __tablename__ = "tendencias_inventario"
    
    id = Column(String, primary_key=True)
    producto_id = Column(String, ForeignKey("productos.id"))
    fecha = Column(DateTime, nullable=False)
    nivel_stock = Column(Integer)
    pronostico_demanda = Column(Integer)  # Basado en IA
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
