"""
Script para generar el diagrama UML (PNG) usando Python.
Requiere internet y la librería plantuml.
"""
import os
import sys

def generar_png():
    # Verificar instalación de librería
    try:
        from plantuml import PlantUML
    except ImportError:
        print("⚠️  Error: Falta la librería 'plantuml'.")
        print("   Por favor ejecuta: pip install plantuml")
        return

    archivo_puml = 'diagrama_clases.puml'
    
    if not os.path.exists(archivo_puml):
        print(f"❌ Error: No se encuentra el archivo {archivo_puml}")
        return

    print(f"🔄 Procesando {archivo_puml}...")
    print("   (Conectando con el servidor de PlantUML...)")

    try:
        # Usar servidor público
        servidor = PlantUML(url='http://www.plantuml.com/plantuml/img/')
        
        # Generar y descargar
        servidor.processes_file(archivo_puml)
        print(f"✅ Imagen generada correctamente: {archivo_puml.replace('.puml', '.png')}")
        
    except Exception as e:
        print(f"❌ Error al generar imagen: {e}")

if __name__ == "__main__":
    generar_png()