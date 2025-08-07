from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.moneda import TasaCambio
from ..database import get_db

router = APIRouter()

@router.get("/convertir")
async def convertir_moneda(
    monto: float,
    origen: str,  # "HTG", "USD", "EUR"
    destino: str,
    db: AsyncSession = Depends(get_db)
):
    tasa = await TasaCambio.obtener_tasa(db, origen, destino)
    return {
        "monto_original": monto,
        "monto_convertido": monto * tasa,
        "moneda": destino
    }
