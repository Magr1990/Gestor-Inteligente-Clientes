"""
Sistema de logging para el GIC
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

class Logger:
    """Sistema de logging personalizado para GIC"""
    
    def __init__(self, log_dir="logs", app_name="gic"):
        self.log_dir = log_dir
        self.app_name = app_name
        self._setup_logging()
    
    def _setup_logging(self):
        """Configura el sistema de logging"""
        try:
            # Crear directorio de logs si no existe
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)
            
            # Configurar logger principal
            self.logger = logging.getLogger('GIC')
            self.logger.setLevel(logging.DEBUG)
            
            # Evitar propagación al logger root
            self.logger.propagate = False
            
            # Crear formateador
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            # Handler para archivo (rotativo)
            log_file = os.path.join(self.log_dir, f"{self.app_name}.log")
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10485760,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            
            # Handler para consola
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            
            # Agregar handlers al logger
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
            
            # Log inicial
            self.logger.info("Sistema de logging inicializado")
            
        except Exception as e:
            print(f"Error al configurar logging: {e}")
            # Fallback a logging básico
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger('GIC_FALLBACK')
    
    def log(self, mensaje, nivel="INFO"):
        """Registra un mensaje en el log"""
        nivel = nivel.upper()
        
        if nivel == "DEBUG":
            self.logger.debug(mensaje)
        elif nivel == "INFO":
            self.logger.info(mensaje)
        elif nivel == "WARNING":
            self.logger.warning(mensaje)
        elif nivel == "ERROR":
            self.logger.error(mensaje)
        elif nivel == "CRITICAL":
            self.logger.critical(mensaje)
        else:
            self.logger.info(mensaje)
    
    def log_operacion(self, usuario, operacion, detalles=""):
        """Registra una operación específica del sistema"""
        mensaje = f"Usuario: {usuario} - Operación: {operacion}"
        if detalles:
            mensaje += f" - Detalles: {detalles}"
        
        self.log(mensaje, "INFO")
    
    def log_error_detallado(self, excepcion, contexto=""):
        """Registra un error con detalles"""
        mensaje = f"Excepción: {type(excepcion).__name__} - Mensaje: {str(excepcion)}"
        if contexto:
            mensaje += f" - Contexto: {contexto}"
        
        self.log(mensaje, "ERROR")
    
    def obtener_logs_recientes(self, lineas=50):
        """Obtiene los logs más recientes"""
        try:
            log_file = os.path.join(self.log_dir, f"{self.app_name}.log")
            
            if not os.path.exists(log_file):
                return ["Archivo de log no encontrado"]
            
            with open(log_file, 'r', encoding='utf-8') as f:
                todas_lineas = f.readlines()
                lineas_recientes = todas_lineas[-lineas:] if len(todas_lineas) > lineas else todas_lineas
            
            return lineas_recientes
            
        except Exception as e:
            return [f"Error al leer logs: {str(e)}"]
    
    def crear_backup_logs(self):
        """Crea un backup de los logs actuales"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.log_dir, f"backup_logs_{timestamp}.log")
            
            log_file = os.path.join(self.log_dir, f"{self.app_name}.log")
            
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as origen:
                    with open(backup_file, 'w', encoding='utf-8') as destino:
                        destino.write(origen.read())
                
                self.log(f"Backup de logs creado: {backup_file}", "INFO")
                return backup_file
            
            return None
            
        except Exception as e:
            self.log(f"Error al crear backup de logs: {str(e)}", "ERROR")
            return None
    
    def limpiar_logs_antiguos(self, dias=30):
        """Elimina logs más antiguos que el número especificado de días"""
        try:
            import time
            
            ahora = time.time()
            limite = dias * 24 * 60 * 60  # Convertir días a segundos
            
            for archivo in os.listdir(self.log_dir):
                if archivo.startswith("backup_logs_") and archivo.endswith(".log"):
                    ruta_archivo = os.path.join(self.log_dir, archivo)
                    
                    # Obtener tiempo de modificación
                    tiempo_mod = os.path.getmtime(ruta_archivo)
                    
                    # Verificar si es más antiguo que el límite
                    if (ahora - tiempo_mod) > limite:
                        os.remove(ruta_archivo)
                        self.log(f"Log antiguo eliminado: {archivo}", "INFO")
            
            return True
            
        except Exception as e:
            self.log(f"Error al limpiar logs antiguos: {str(e)}", "ERROR")
            return False