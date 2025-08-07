import httpx
from decimal import Decimal

class ConversorMoneda:
    def __init__(self):
        self.cache = {}
    
    async def obtener_tasa_cambio(self, moneda_origen: str, moneda_destino: str) -> Decimal:
        if moneda_origen == moneda_destino:
            return Decimal("1.0")
        
        clave_cache = f"{moneda_origen}_{moneda_destino}"
        if clave_cache in self.cache:
            return self.cache[clave_cache]
        
        # Ejemplo: API del Banco Central de Haití
        async with httpx.AsyncClient() as cliente:
            respuesta = await cliente.get(
                f"https://api.bancentral.gov.do/tasas/{moneda_origen}/{moneda_destino}"
            )
            tasa = Decimal(respuesta.json()["tasa"])
        
        self.cache[clave_cache] = tasa
        return tasa

# Uso en endpoint
@router.get("/convertir")
async def convertir_moneda(
    monto: float,
    moneda_origen: str,
    moneda_destino: str,
    conversor: ConversorMoneda = Depends()
):
    tasa = await conversor.obtener_tasa_cambio(moneda_origen, moneda_destino)
    return {
        "monto_original": monto,
        "monto_convertido": float(Decimal(monto) * tasa),
        "moneda": moneda_destino
    }
