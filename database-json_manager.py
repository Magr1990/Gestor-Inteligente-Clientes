"""
Gestor de archivos JSON para backup y exportación
"""

import json
import csv
import os
from datetime import datetime

class JSONManager:
    """Manejador de archivos JSON para clientes"""
    
    def __init__(self, backup_dir="backups"):
        self.backup_dir = backup_dir
        self._crear_directorio()
    
    def _crear_directorio(self):
        """Crea el directorio de backups si no existe"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def exportar_clientes(self, clientes, nombre_archivo=None):
        """Exporta clientes a archivo JSON"""
        if not nombre_archivo:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"clientes_export_{timestamp}.json"
        
        ruta_completa = os.path.join(self.backup_dir, nombre_archivo)
        
        try:
            # Convertir clientes a diccionarios
            clientes_dict = []
            for cliente in clientes:
                info = cliente.obtener_informacion()
                
                # Agregar datos específicos según tipo
                if hasattr(cliente, 'puntos_fidelidad'):
                    info['puntos_fidelidad'] = cliente.puntos_fidelidad
                elif hasattr(cliente, 'nivel'):
                    info['nivel'] = cliente.nivel
                    info['beneficios_extra'] = cliente.beneficios_extra
                elif hasattr(cliente, 'empresa'):
                    info['empresa'] = cliente.empresa
                    info['nit'] = cliente.nit
                    info['contacto_alterno'] = cliente.contacto_alterno
                    info['facturacion_mensual'] = cliente.facturacion_mensual
                
                clientes_dict.append(info)
            
            # Guardar en archivo JSON
            with open(ruta_completa, 'w', encoding='utf-8') as f:
                json.dump(clientes_dict, f, indent=2, default=str)
            
            return ruta_completa
            
        except Exception as e:
            print(f"Error al exportar clientes: {e}")
            return None
    
    def exportar_clientes_csv(self, clientes, nombre_archivo=None):
        """Exporta clientes a archivo CSV"""
        if not nombre_archivo:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"clientes_export_{timestamp}.csv"
        
        ruta_completa = os.path.join(self.backup_dir, nombre_archivo)
        
        try:
            if not clientes:
                return None

            # Definir encabezados (campos comunes + específicos)
            fieldnames = ['id', 'nombre', 'email', 'telefono', 'direccion', 
                          'tipo', 'fecha_registro', 'activo', 
                          'puntos_fidelidad', 'nivel', 'beneficios_extra',
                          'empresa', 'nit', 'contacto_alterno', 'facturacion_mensual']
            
            with open(ruta_completa, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for cliente in clientes:
                    info = cliente.obtener_informacion()
                    # Aplanar datos específicos para CSV
                    if hasattr(cliente, 'puntos_fidelidad'):
                        info['puntos_fidelidad'] = cliente.puntos_fidelidad
                    elif hasattr(cliente, 'nivel'):
                        info['nivel'] = cliente.nivel
                        info['beneficios_extra'] = "|".join(cliente.beneficios_extra) # Lista a string
                    elif hasattr(cliente, 'empresa'):
                        info['empresa'] = cliente.empresa
                        info['nit'] = cliente.nit
                        info['contacto_alterno'] = cliente.contacto_alterno
                        info['facturacion_mensual'] = cliente.facturacion_mensual
                    
                    # Rellenar campos faltantes con vacío para mantener estructura
                    row = {k: info.get(k, '') for k in fieldnames}
                    writer.writerow(row)
            
            return ruta_completa
            
        except Exception as e:
            print(f"Error al exportar CSV: {e}")
            return None

    def importar_clientes(self, ruta_archivo):
        """Importa clientes desde archivo JSON"""
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                clientes_dict = json.load(f)
            
            # Reconstruir objetos Cliente (solo datos, sin instancias)
            # En una implementación real, se crearían las instancias apropiadas
            return clientes_dict
            
        except Exception as e:
            print(f"Error al importar clientes: {e}")
            return []
    
    def crear_backup(self, db_manager):
        """Crea un backup completo de la base de datos"""
        try:
            clientes = db_manager.obtener_todos_clientes()
            if not clientes:
                return None
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_backup = f"backup_completo_{timestamp}.json"
            
            ruta_backup = self.exportar_clientes(clientes, nombre_backup)
            
            # Registrar backup
            logs = db_manager.obtener_logs(50)
            info_backup = {
                "fecha": datetime.now().isoformat(),
                "total_clientes": len(clientes),
                "archivo": nombre_backup,
                "ultimos_logs": logs
            }
            
            ruta_info = os.path.join(self.backup_dir, f"info_backup_{timestamp}.json")
            with open(ruta_info, 'w', encoding='utf-8') as f:
                json.dump(info_backup, f, indent=2, default=str)
            
            return ruta_backup
            
        except Exception as e:
            print(f"Error al crear backup: {e}")
            return None
    
    def listar_backups(self):
        """Lista todos los backups disponibles"""
        try:
            backups = []
            for archivo in os.listdir(self.backup_dir):
                if archivo.startswith("clientes_export_") or archivo.startswith("backup_completo_"):
                    ruta = os.path.join(self.backup_dir, archivo)
                    tamaño = os.path.getsize(ruta)
                    fecha_mod = datetime.fromtimestamp(os.path.getmtime(ruta))
                    
                    backups.append({
                        'nombre': archivo,
                        'ruta': ruta,
                        'tamaño': tamaño,
                        'fecha_modificacion': fecha_mod
                    })
            
            return sorted(backups, key=lambda x: x['fecha_modificacion'], reverse=True)
            
        except Exception as e:
            print(f"Error al listar backups: {e}")
            return []