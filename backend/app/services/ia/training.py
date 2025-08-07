import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import InventoryMovement, Product

async def train_demand_model(db: AsyncSession, product_id: str = None):
    # Obtener datos históricos (últimos 2 años)
    date_threshold = datetime.now() - timedelta(days=730)
    
    query = select(
        InventoryMovement.created_at,
        InventoryMovement.product_id,
        InventoryMovement.type,
        InventoryMovement.quantity,
        Product.category
    ).join(
        Product, InventoryMovement.product_id == Product.id
    ).where(
        InventoryMovement.created_at >= date_threshold
    )
    
    if product_id:
        query = query.where(InventoryMovement.product_id == product_id)
    
    result = await db.execute(query)
    data = result.all()
    
    # Convertir a DataFrame
    df = pd.DataFrame([{
        'date': mov.created_at,
        'product_id': mov.product_id,
        'type': mov.type,
        'quantity': mov.quantity,
        'category': mov.category,
        'day_of_week': mov.created_at.weekday(),
        'month': mov.created_at.month,
        'is_weekend': mov.created_at.weekday() >= 5
    } for mov in data])
    
    # Procesamiento de datos
    df['net_quantity'] = df.apply(
        lambda x: x['quantity'] if x['type'] == 'entrada' else -x['quantity'], 
        axis=1
    )
    
    # Agregar por día y producto
    daily_data = df.groupby(
        [pd.Grouper(key='date', freq='D'), 'product_id']
    )['net_quantity'].sum().reset_index()
    
    # Preparar características
    X = daily_data[['product_id', 'date']].copy()
    X['day_of_week'] = X['date'].dt.weekday
    X['month'] = X['date'].dt.month
    X['is_weekend'] = X['day_of_week'] >= 5
    X = pd.get_dummies(X, columns=['product_id'])
    
    y = daily_data['net_quantity']
    
    # Entrenar modelo
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Guardar modelo
    model_path = f"models/demand_model_{datetime.now().strftime('%Y%m%d')}.pkl"
    joblib.dump(model, model_path)
    
    return {
        'model_path': model_path,
        'test_score': model.score(X_test, y_test),
        'products_trained': X['product_id'].nunique()
    }
