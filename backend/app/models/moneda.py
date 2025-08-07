from sqlalchemy import Column, String, Numeric, DateTime
from sqlalchemy.sql import func
from .base import Base

class TasaCambio(Base):
    __tablename__ = "tasas_cambio"
    
    id = Column(String, primary_key=True)
    par_moneda = Column(String(6))  # Ej: "HTG_USD"
    tasa = Column(Numeric(10, 4))   # 1 HTG = X USD
    actualizado_en = Column(DateTime, server_default=func.now())

    @classmethod
    async def obtener_tasa(cls, sesion, moneda_origen: str, moneda_destino: str):
        if moneda_origen == moneda_destino:
            return 1.0
        par = f"{moneda_origen}_{moneda_destino}"
        resultado = await sesion.execute(select(cls.tasa).where(cls.par_moneda == par))
        return resultado.scalar() or 1.0  # Default 1:1 si no hay tasa
