from fastapi_i18n import I18nMiddleware, I18n
from pathlib import Path
from fastapi import Request

class GestorI18N:
    def __init__(self):
        self.i18n = I18nMiddleware(
            default_locale="es",
            locales=["es", "en", "fr", "ht"],  # Español, Inglés, Francés, Criollo Haitiano
            directory=Path("locales")  # Carpeta con archivos JSON de traducción
        )
    
    def traducir(self, clave: str, request: Request, **kwargs):
        locale = request.headers.get("Accept-Language", "es")
        return self.i18n._(clave, locale=locale, **kwargs)

# Ejemplo de uso en endpoints:
@router.get("/producto")
async def obtener_producto(request: Request):
    gestor = GestorI18N()
    return {
        "nombre": gestor.traducir("nombre_producto", request),
        "precio": gestor.traducir("precio_htg", request, cantidad=1000)
    }
