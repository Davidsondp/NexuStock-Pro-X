# backend/app/servicios/traducciones.py
from fastapi import Request
from fastapi_i18n import I18nMiddleware, lazy_gettext as _

i18n = I18nMiddleware(
    default_locale="es",
    locales=["es", "en", "fr", "ht"],  # Español, Inglés, Francés, Criollo Haitiano
    loader=FileSystemLoader("backend/static/locales")
)

def get_text(request: Request, key: str) -> str:
    return _(key, request=request)

# Ejemplo de uso en endpoints
@router.get("/producto/{id}")
async def get_producto(id: str, request: Request):
    return {"nombre": get_text(request, "product_name")}
