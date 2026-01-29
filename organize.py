"""
Script para organizar automáticamente la estructura del proyecto GIC
"""
import os
import shutil

def organizar_proyecto():
    # Mapeo de archivos actuales a su ubicación destino
    # Formato: "nombre_actual": ("carpeta_destino", "nombre_nuevo")
    archivos = {
        "Interfaz Gráfica.py": ("gui", "main_window.py"),
        "database-db_manager.py": ("database", "db_manager.py"),
        "database-json_manager.py": ("database", "json_manager.py"),
        "models-cliente.py": ("models", "cliente.py"),
        "models-cliente_regular.py": ("models", "cliente_regular.py"),
        "models-cliente_premium.py": ("models", "cliente_premium.py"),
        "models-cliente_corporativo.py": ("models", "cliente_corporativo.py"),
        "utils-logger.py": ("utils", "logger.py"),
        "utils-validators.py": ("utils", "validators.py"),
        "api_integrations-email_validator.py": ("api_integrations", "email_validator.py"),
        "api_integrations-notification_service.py": ("api_integrations", "notification_service.py"),
        "teststest_clientes.py": ("tests", "test_clientes.py"),
    }

    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Organizando archivos en: {base_dir}")

    # Crear carpetas y mover archivos
    for archivo_actual, (carpeta, nuevo_nombre) in archivos.items():
        # Ruta completa del archivo actual
        ruta_actual = os.path.join(base_dir, archivo_actual)
        
        # Ruta destino
        dir_destino = os.path.join(base_dir, carpeta)
        ruta_destino = os.path.join(dir_destino, nuevo_nombre)

        # Si el archivo fuente existe
        if os.path.exists(ruta_actual):
            # Crear carpeta si no existe
            if not os.path.exists(dir_destino):
                os.makedirs(dir_destino)
                
                # Crear __init__.py para que sea un paquete Python
                init_path = os.path.join(dir_destino, "__init__.py")
                if not os.path.exists(init_path):
                    with open(init_path, 'w') as f:
                        pass

            # Mover archivo
            try:
                shutil.move(ruta_actual, ruta_destino)
                print(f"✅ Movido: {archivo_actual} -> {carpeta}/{nuevo_nombre}")
            except Exception as e:
                print(f"❌ Error moviendo {archivo_actual}: {e}")
        
        elif os.path.exists(ruta_destino):
            print(f"ℹ️ Ya existe: {carpeta}/{nuevo_nombre}")

    print("\nOrganización completada.")

if __name__ == "__main__":
    organizar_proyecto()