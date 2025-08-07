from fastapi_i18n import I18nMiddleware, Translator
from pathlib import Path
from typing import Dict

class ServicioI18N:
    def __init__(self):
        self.traductor = Translator(
            directorio_locales=[Path("locales")],
            idioma_predeterminado="es",
            idiomas_soportados=["es", "en", "fr", "ht", "pt", "zh", "ar"]
        )
    
    def traducir(self, clave: str, idioma: str, **kwargs) -> str:
        return self.traductor.translate(clave, locale=idioma, **kwargs)

# Ejemplo de uso en endpoints
@router.get("/bienvenida")
async def bienvenida_usuario(idioma: str = Header("es")):
    i18n = ServicioI18N()
    return {
        "mensaje": i18n.traducir("mensaje_bienvenida", idioma),
        "moneda": i18n.traducir("moneda", idioma, moneda="HTG")
    }
