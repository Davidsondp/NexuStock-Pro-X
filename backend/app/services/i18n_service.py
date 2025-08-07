from fastapi_i18n import I18nMiddleware, Translator
from pathlib import Path
from typing import Dict

class I18N:
    def __init__(self):
        self.translator = Translator(
            locale_dirs=[Path("locales")],
            default_locale="es",
            supported_locales=["es", "en", "fr", "ht", "pt", "zh", "ar", "sw"]
        )
    
    def translate(self, key: str, locale: str, **kwargs) -> str:
        return self.translator.translate(key, locale=locale, **kwargs)

# Ejemplo de uso en endpoints
@router.get("/welcome")
async def welcome_user(locale: str = Header("es")):
    i18n = I18N()
    return {
        "message": i18n.translate("welcome_message", locale),
        "currency": i18n.translate("currency", locale, currency="HTG")
    }
