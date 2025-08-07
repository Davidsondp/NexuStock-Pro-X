from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..services.ai.training import train_demand_model
from ..services.ai.prediction import DemandPredictor
from ..database import get_db
from ..utils.security import is_admin

router = APIRouter()
predictor = None

@router.post("/train-model")
async def train_model(
    product_id: str = None,
    db: AsyncSession = Depends(get_db),
    _ = Depends(is_admin)
):
    try:
        result = await train_demand_model(db, product_id)
        global predictor
        predictor = DemandPredictor(result['model_path'])
        return result
    except Exception as e:
        raise HTTPException(500, f"Error en entrenamiento: {str(e)}")

@router.get("/predict-demand/{product_id}")
async def predict_demand(
    product_id: str,
    days: int = 30,
    db: AsyncSession = Depends(get_db),
    _ = Depends(is_admin)
):
    if not predictor:
        raise HTTPException(400, "Modelo no entrenado. Entrene un modelo primero")
    
    try:
        return await predictor.predict(product_id, days, db)
    except Exception as e:
        raise HTTPException(500, f"Error en predicción: {str(e)}")

@router.get("/stock-alerts")
async def get_stock_alerts(
    threshold: float = 0.3,  # 30% del stock actual
    db: AsyncSession = Depends(get_db),
    _ = Depends(is_admin)
):
    if not predictor:
        raise HTTPException(400, "Modelo no entrenado")
    
    # Obtener todos los productos
    products = await db.execute(select(Product))
    alerts = []
    
    for product in products.scalars():
        prediction = await predictor.predict(product.id, 30, db)
        if prediction['recommendation']['action'] != 'monitor':
            alerts.append({
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'current_stock': product.stock
                },
                'prediction': prediction
            })
    
    return alerts
