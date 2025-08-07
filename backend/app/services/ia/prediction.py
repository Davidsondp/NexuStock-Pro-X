import pandas as pd
import joblib
from datetime import datetime, timedelta

class DemandPredictor:
    def __init__(self, model_path: str):
        self.model = joblib.load(model_path)
        self.last_trained = datetime.now()
    
    async def predict(
        self, 
        product_id: str, 
        days: int = 30,
        db: AsyncSession = None
    ) -> dict:
        # Generar fechas futuras
        dates = [datetime.now() + timedelta(days=i) for i in range(1, days+1)]
        
        # Preparar datos de entrada
        X_pred = pd.DataFrame({
            'date': dates,
            'product_id': product_id
        })
        X_pred['day_of_week'] = X_pred['date'].dt.weekday
        X_pred['month'] = X_pred['date'].dt.month
        X_pred['is_weekend'] = X_pred['day_of_week'] >= 5
        X_pred = pd.get_dummies(X_pred, columns=['product_id'])
        
        # Hacer predicciones
        predictions = self.model.predict(X_pred)
        
        # Obtener datos actuales del producto
        if db:
            product = await db.get(Product, product_id)
            current_stock = product.stock if product else 0
        else:
            current_stock = 0
        
        # Calcular proyección de stock
        stock_projection = [current_stock]
        for qty in predictions:
            stock_projection.append(stock_projection[-1] + qty)
        
        return {
            'product_id': product_id,
            'predictions': predictions.tolist(),
            'stock_projection': stock_projection[1:],
            'critical_day': self._find_critical_day(stock_projection),
            'recommendation': self._generate_recommendation(
                current_stock, 
                predictions.sum()
            )
        }
    
    def _find_critical_day(self, projection):
        for i, stock in enumerate(projection):
            if stock <= 0:
                return i + 1  # Días desde hoy
        return None
    
    def _generate_recommendation(self, current_stock, predicted_change):
        net_stock = current_stock + predicted_change
        if net_stock < 0:
            return {
                'action': 'urgent_order',
                'quantity': abs(predicted_change) * 1.2,  # 20% extra
                'message': 'Necesita reabastecimiento urgente'
            }
        elif net_stock < (current_stock * 0.3):  # Menos del 30% del stock actual
            return {
                'action': 'order',
                'quantity': abs(predicted_change),
                'message': 'Sugerencia de reabastecimiento'
            }
        else:
            return {
                'action': 'monitor',
                'quantity': 0,
                'message': 'Stock suficiente'
            }
