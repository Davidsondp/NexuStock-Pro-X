from gtts import gTTS
from io import BytesIO
from fastapi.responses import StreamingResponse

class SintetizadorVoz:
    def __init__(self):
        self.voices = {
            "es": "es-ES",  # Español
            "ht": "ht-HT",  # Criollo Haitiano
            "en": "en-US"
        }
    
    def generar_audio(self, texto: str, idioma: str = "es"):
        tts = gTTS(text=texto, lang=self.voices.get(idioma, "es"))
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes

# Uso en endpoint:
@router.get("/hablar")
async def hablar(texto: str, idioma: str = "es"):
    voz = SintetizadorVoz()
    audio = voz.generar_audio(texto, idioma)
    return StreamingResponse(audio, media_type="audio/mpeg")
