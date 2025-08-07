import httpx
from decimal import Decimal
from datetime import datetime

class CurrencyConverter:
    def __init__(self):
        self.cache = {}
    
    async def get_exchange_rate(self, from_curr: str, to_curr: str) -> Decimal:
        if from_curr == to_curr:
            return Decimal("1.0")
        
        cache_key = f"{from_curr}_{to_curr}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # API de bancos centrales (ejemplo: Banco de la República de Haití)
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.bancentral.gov.do/rates/{from_curr}/{to_curr}"
            )
            rate = Decimal(response.json()["rate"])
        
        self.cache[cache_key] = rate
        return rate

# Uso en endpoints
@router.get("/convert")
async def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str,
    converter: CurrencyConverter = Depends()
):
    rate = await converter.get_exchange_rate(from_currency, to_currency)
    return {
        "original_amount": amount,
        "converted_amount": float(Decimal(amount) * rate),
        "currency": to_currency
    }
