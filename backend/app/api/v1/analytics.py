from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from ..services.servicio_analitica import (
    generar_reporte_ventas,
    calcular_rotacion_inventario
)
from ..database import get_db

router = APIRouter()

@router.get("/ventas")
async def obtener_analitica_ventas(
    fecha_inicio: datetime = Query(default_factory=lambda: datetime.now() - timedelta(days=30)),
    fecha_fin: datetime = Query(default_factory=datetime.now),
    categoria: str = None,
    db: AsyncSession = Depends(get_db)
):
    reporte = await generar_reporte_ventas(db, fecha_inicio, fecha_fin, categoria)
    return reporte.to_dict("records")

@router.get("/inventario/rotacion")
async def obtener_rotacion_inventario(
    producto_id: str = None,
    db: AsyncSession = Depends(get_db)
):
    rotacion = await calcular_rotacion_inventario(db, producto_id)
    return rotacion.to_dict("records")
