import pyttsx3
from io import BytesIO

class ServicioVoz:
    def __init__(self):
        self.motor = pyttsx3.init()
        self.voces = {
            'es': 'spanish-latin-am',
            'ht': 'mb-haitian',
            'en': 'english-us',
            'fr': 'french'
        }
    
    def texto_a_voz(self, texto: str, idioma: str) -> BytesIO:
        self.motor.setProperty('voice', self.voces.get(idioma, 'english-us'))
        
        salida = BytesIO()
        self.motor.save_to_file(texto, salida.name)
        self.motor.runAndWait()
        
        salida.seek(0)
        return salida

# Endpoint de voz
@router.get("/hablar")
async def hablar_texto(
    texto: str,
    idioma: str = "es",
    voz: ServicioVoz = Depends()
):
    audio = voz.texto_a_voz(texto, idioma)
    return StreamingResponse(
        audio,
        media_type="audio/wav",
        headers={"Content-Disposition": "inline"}
    )
