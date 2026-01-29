"""
Gestor de base de datos SQLite para clientes
"""

import sqlite3
import json
from datetime import datetime
from models.cliente_regular import ClienteRegular
from models.cliente_premium import ClientePremium
from models.cliente_corporativo import ClienteCorporativo

class DatabaseManager:
    """Manejador de la base de datos SQLite"""
    
    def __init__(self, db_name="clientes.db"):
        self.db_name = db_name
        self._init_database()
    
    def _init_database(self):
        """Inicializa la base de datos con las tablas necesarias"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Tabla de clientes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY,
                    tipo TEXT NOT NULL,
                    nombre TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    telefono TEXT NOT NULL,
                    direccion TEXT NOT NULL,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    activo BOOLEAN DEFAULT 1,
                    datos_especificos TEXT
                )
            ''')
            
            # Tabla de logs
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    accion TEXT NOT NULL,
                    detalles TEXT,
                    usuario TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except sqlite3.Error as e:
            print(f"Error al inicializar la base de datos: {e}")
            raise
    
    def guardar_cliente(self, cliente):
        """Guarda un cliente en la base de datos"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Preparar datos específicos según tipo
            datos_especificos = self._serializar_datos_especificos(cliente)
            
            cursor.execute('''
                INSERT OR REPLACE INTO clientes 
                (id, tipo, nombre, email, telefono, direccion, datos_especificos)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                cliente.id,
                cliente.obtener_tipo(),
                cliente.nombre,
                cliente.email,
                cliente.telefono,
                cliente.direccion,
                datos_especificos
            ))
            
            conn.commit()
            conn.close()
            
            # Registrar en logs
            self._log_accion("CLIENTE_GUARDADO", f"Cliente {cliente.id} - {cliente.nombre}")
            
            return True
            
        except sqlite3.Error as e:
            print(f"Error al guardar cliente: {e}")
            return False
    
    def _serializar_datos_especificos(self, cliente):
        """Serializa los datos específicos según el tipo de cliente"""
        datos = {}
        
        if isinstance(cliente, ClienteRegular):
            datos['puntos_fidelidad'] = cliente.puntos_fidelidad
            
        elif isinstance(cliente, ClientePremium):
            datos['nivel'] = cliente.nivel
            datos['beneficios_extra'] = cliente.beneficios_extra
            
        elif isinstance(cliente, ClienteCorporativo):
            datos['empresa'] = cliente.empresa
            datos['nit'] = cliente.nit
            datos['contacto_alterno'] = cliente.contacto_alterno
            datos['facturacion_mensual'] = cliente.facturacion_mensual
        
        return json.dumps(datos)
    
    def cargar_cliente(self, cliente_id):
        """Carga un cliente desde la base de datos"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM clientes WHERE id = ?', (cliente_id,))
            row = cursor.fetchone()
            
            conn.close()
            
            if not row:
                return None
            
            return self._deserializar_cliente(row)
            
        except sqlite3.Error as e:
            print(f"Error al cargar cliente: {e}")
            return None
    
    def _deserializar_cliente(self, row):
        """Deserializa una fila de la base de datos a un objeto Cliente"""
        (cliente_id, tipo, nombre, email, telefono, direccion, 
         fecha_registro, activo, datos_especificos) = row
        
        datos = json.loads(datos_especificos) if datos_especificos else {}
        
        # Convertir fecha_registro de string a datetime
        fecha_reg_obj = None
        if fecha_registro:
            try:
                fecha_reg_obj = datetime.strptime(fecha_registro, "%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                fecha_reg_obj = None

        # Determinar el tipo de cliente
        if "Regular" in tipo:
            cliente = ClienteRegular(
                cliente_id, nombre, email, telefono, direccion,
                datos.get('puntos_fidelidad', 0),
                fecha_registro=fecha_reg_obj
            )
            
        elif "Premium" in tipo:
            cliente = ClientePremium(
                cliente_id, nombre, email, telefono, direccion,
                datos.get('nivel', 'oro'),
                fecha_registro=fecha_reg_obj
            )
            for beneficio in datos.get('beneficios_extra', []):
                cliente.agregar_beneficio(beneficio)
                
        elif "Corporativo" in tipo:
            cliente = ClienteCorporativo(
                cliente_id, nombre, email, telefono, direccion,
                datos.get('empresa', ''),
                datos.get('nit', ''),
                datos.get('contacto_alterno', None),
                fecha_registro=fecha_reg_obj
            )
            cliente.actualizar_facturacion(datos.get('facturacion_mensual', 0))
        
        else:
            return None
        
        cliente.activo = bool(activo)
        return cliente
    
    def obtener_todos_clientes(self):
        """Obtiene todos los clientes de la base de datos"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM clientes ORDER BY nombre')
            rows = cursor.fetchall()
            
            conn.close()
            
            clientes = []
            for row in rows:
                cliente = self._deserializar_cliente(row)
                if cliente:
                    clientes.append(cliente)
            
            return clientes
            
        except sqlite3.Error as e:
            print(f"Error al obtener clientes: {e}")
            return []
    
    def eliminar_cliente(self, cliente_id):
        """Elimina un cliente de la base de datos"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
            conn.commit()
            
            deleted = cursor.rowcount > 0
            conn.close()
            
            if deleted:
                self._log_accion("CLIENTE_ELIMINADO", f"Cliente {cliente_id}")
            
            return deleted
            
        except sqlite3.Error as e:
            print(f"Error al eliminar cliente: {e}")
            return False
    
    def buscar_clientes(self, criterio, valor):
        """Busca clientes por criterio"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            query = f"SELECT * FROM clientes WHERE {criterio} LIKE ? ORDER BY nombre"
            cursor.execute(query, (f'%{valor}%',))
            
            rows = cursor.fetchall()
            conn.close()
            
            clientes = []
            for row in rows:
                cliente = self._deserializar_cliente(row)
                if cliente:
                    clientes.append(cliente)
            
            return clientes
            
        except sqlite3.Error as e:
            print(f"Error en búsqueda: {e}")
            return []
    
    def _log_accion(self, accion, detalles=""):
        """Registra una acción en la tabla de logs"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO logs (accion, detalles, timestamp)
                VALUES (?, ?, ?)
            ''', (accion, detalles, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
        except sqlite3.Error:
            pass
    
    def obtener_logs(self, limite=100):
        """Obtiene los últimos logs"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM logs 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limite,))
            
            logs = cursor.fetchall()
            conn.close()
            
            return logs
            
        except sqlite3.Error as e:
            print(f"Error al obtener logs: {e}")
            return []