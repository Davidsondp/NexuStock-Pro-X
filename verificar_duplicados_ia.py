import os
import hashlib
from collections import defaultdict
from difflib import get_close_matches
from itertools import combinations
import openai
from dotenv import load_dotenv

# 📌 Configuraciones
ROOT_DIR = '.'  # Raíz del proyecto
SIMILARITY_THRESHOLD = 0.85
MAX_CONTENT_PREVIEW = 12000
INFORME_PATH = 'informe_proyecto.txt'

# Cargar clave API de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Utilidades
def hash_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def leer_archivo(ruta):
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ""

# 🔍 Buscar duplicados por nombre
def buscar_duplicados_por_nombre():
    resultado = ["\n🔍 Archivos con NOMBRES duplicados:"]
    nombre_archivos = defaultdict(list)
    for root, _, files in os.walk(ROOT_DIR):
        for file in files:
            nombre_archivos[file].append(os.path.join(root, file))
    for nombre, rutas in nombre_archivos.items():
        if len(rutas) > 1:
            resultado.append(f"  - {nombre} ({len(rutas)} veces):")
            for ruta in rutas:
                resultado.append(f"    → {ruta}")
    return "\n".join(resultado)

# 🧬 Buscar duplicados por contenido
def buscar_duplicados_por_contenido():
    resultado = ["\n🧬 Archivos con CONTENIDO duplicado (hash):"]
    hashes = defaultdict(list)
    for root, _, files in os.walk(ROOT_DIR):
        for file in files:
            path = os.path.join(root, file)
            h = hash_file(path)
            if h:
                hashes[h].append(path)
    for h, paths in hashes.items():
        if len(paths) > 1:
            resultado.append(f"  - Hash: {h[:10]} ({len(paths)} archivos):")
            for p in paths:
                resultado.append(f"    → {p}")
    return "\n".join(resultado)

# 📁 Buscar carpetas con nombres similares
def buscar_carpetas_similares():
    resultado = ["\n📁 Carpetas con nombres similares:"]
    carpetas = []
    for root, dirs, _ in os.walk(ROOT_DIR):
        for d in dirs:
            if d not in carpetas:
                similares = get_close_matches(d, carpetas, n=5, cutoff=SIMILARITY_THRESHOLD)
                for s in similares:
                    if d.lower() != s.lower():
                        resultado.append(f"  - '{d}' ≈ '{s}'")
                carpetas.append(d)
    return "\n".join(resultado)

# 🤖 Comparar funcionalidad entre archivos con OpenAI
def comparar_con_openai(archivo1, archivo2, contenido1, contenido2):
    prompt = f"""
Analiza los siguientes dos archivos Python y responde con 'IGUALES' si hacen esencialmente lo mismo (aunque estén en diferentes idiomas o tengan nombres distintos), o responde 'DIFERENTES' si son funcionalmente distintos.

Archivo 1:
{contenido1}

Archivo 2:
{contenido2}

Respuesta:
"""
    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=10
        )
        return respuesta.choices[0].message.content.strip()
    except Exception as e:
        return f"ERROR: {e}"

def detectar_duplicados_funcionales():
    archivos = []
    resultado = ["\n🤖 Duplicados FUNCIONALES detectados por IA:"]
    for root, _, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith('.py'):
                archivos.append(os.path.join(root, file))

    comparados = set()
    for archivo1, archivo2 in combinations(archivos, 2):
        if (archivo2, archivo1) in comparados:
            continue
        cont1 = leer_archivo(archivo1)[:1500]
        cont2 = leer_archivo(archivo2)[:1500]
        if cont1 and cont2:
            resultado_ia = comparar_con_openai(archivo1, archivo2, cont1, cont2)
            if "IGUALES" in resultado_ia.upper():
                resultado.append(f"  ⚠️ POSIBLE DUPLICADO entre:\n    → {archivo1}\n    → {archivo2}")
            comparados.add((archivo1, archivo2))
    return "\n".join(resultado)

# 🧠 Análisis general del proyecto
def analizar_estado_general_proyecto():
    resumen = ""
    for root, _, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith('.py') or file.endswith('.html'):
                ruta = os.path.join(root, file)
                contenido = leer_archivo(ruta)
                resumen += f"\nArchivo: {ruta}\n{contenido[:800]}\n"

    prompt = f"""
Eres un experto en desarrollo de sistemas web con Flask. A continuación, se presenta una muestra de código y estructura de un sistema de inventario avanzado. Analiza el proyecto y responde con:

1. ✅ Qué funcionalidades ya están implementadas
2. ❌ Qué funcionalidades faltan para que el sistema esté completo y profesional
3. 📌 Recomendaciones clave para completarlo con éxito

Proyecto:
{resumen[:MAX_CONTENT_PREVIEW]}

Responde en forma de informe breve y estructurado.
"""
    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=800
        )
        return "\n📋 INFORME DEL PROYECTO:\n" + respuesta.choices[0].message.content.strip()
    except Exception as e:
        return f"\nERROR al generar informe: {e}"

# 🧠 EJECUCIÓN PRINCIPAL
def main():
    print("🔎 Ejecutando análisis completo del proyecto...\n")
    informe = []

    informe.append(buscar_duplicados_por_nombre())
    informe.append(buscar_duplicados_por_contenido())
    informe.append(buscar_carpetas_similares())
    informe.append(detectar_duplicados_funcionales())
    informe.append(analizar_estado_general_proyecto())

    print("\n✅ Análisis completado. Guardando informe...")

    with open(INFORME_PATH, 'w', encoding='utf-8') as f:
        f.write("\n\n".join(informe))

    print(f"\n📄 Informe guardado en: {INFORME_PATH}")

if __name__ == "__main__":
    main()
