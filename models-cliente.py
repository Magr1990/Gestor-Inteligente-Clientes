import re
from datetime import datetime
from abc import ABC, abstractmethod

class Cliente(ABC):
    
    def __init__(self, id_cliente, nombre, email, telefono, direccion, rut, fecha_registro=None):
        self._id = self._validar_id(id_cliente)
        self._nombre = self._validar_nombre(nombre)
        self._email = self._validar_email(email)
        self._telefono = self._validar_telefono(telefono)
        self._direccion = self._validar_direccion(direccion)
        self._rut = self._validar_rut(rut)
        self._fecha_registro = fecha_registro or datetime.now()
        self._activo = True
    
    @property
    def id(self):
        return self._id
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor):
        self._nombre = self._validar_nombre(valor)
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, valor):
        self._email = self._validar_email(valor)
    
    @property
    def telefono(self):
        return self._telefono
    
    @telefono.setter
    def telefono(self, valor):
        self._telefono = self._validar_telefono(valor)
    
    @property
    def direccion(self):
        return self._direccion
    
    @direccion.setter
    def direccion(self, valor):
        self._direccion = self._validar_direccion(valor)
    
    @property
    def rut(self):
        return self._rut
    
    @rut.setter
    def rut(self, valor):
        self._rut = self._validar_rut(valor)
    
    @property
    def fecha_registro(self):
        return self._fecha_registro
    
    @property
    def activo(self):
        return self._activo
    
    @activo.setter
    def activo(self, valor):
        if not isinstance(valor, bool):
            raise ValueError("El valor de activo debe ser booleano")
        self._activo = valor
    
    def _validar_id(self, id_cliente):
        if not isinstance(id_cliente, int) or id_cliente <= 0:
            raise ValueError("ID debe ser un número entero positivo")
        return id_cliente
    
    def _validar_nombre(self, nombre):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        if len(nombre.strip()) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres")
        return nombre.strip()
    
    def _validar_email(self, email):
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, email):
            raise ValueError("Formato de email inválido")
        return email
    
    def _validar_telefono(self, telefono):
        telefono_limpio = re.sub(r'[\s\-\(\)]', '', str(telefono))
        
        if not telefono_limpio.isdigit():
            raise ValueError("El teléfono debe contener solo dígitos")
        
        if len(telefono_limpio) < 8 or len(telefono_limpio) > 15:
            raise ValueError("El teléfono debe tener entre 8 y 15 dígitos")
        
        return telefono_limpio
    
    def _validar_direccion(self, direccion):
        if not direccion or not direccion.strip():
            raise ValueError("La dirección no puede estar vacía")
        return direccion.strip()
    
    def _validar_rut(self, rut):
        if not rut or not str(rut).strip():
            raise ValueError("El RUT no puede estar vacío")
        return str(rut).strip()
    
    @abstractmethod
    def calcular_descuento(self, monto):
        pass
    
    @abstractmethod
    def obtener_tipo(self):
        pass
    
    def obtener_informacion(self):
        return {
            'id': self._id,
            'nombre': self._nombre,
            'email': self._email,
            'telefono': self._telefono,
            'direccion': self._direccion,
            'rut': self._rut,
            'tipo': self.obtener_tipo(),
            'fecha_registro': self._fecha_registro,
            'activo': self._activo
        }
    
    def __str__(self):
        return f"{self._nombre} ({self.obtener_tipo()}) - {self._email}"
    
    def __eq__(self, otro):
        if not isinstance(otro, Cliente):
            return False
        return self._id == otro._id
    
    def __repr__(self):
        return f"Cliente(id={self._id}, nombre='{self._nombre}', tipo='{self.obtener_tipo()}')"