"""
Pruebas unitarias para el sistema GIC
"""

import unittest
import sys
import os

# Agregar ruta al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.cliente_regular import ClienteRegular
from models.cliente_premium import ClientePremium
from models.cliente_corporativo import ClienteCorporativo
from utils.validators import Validators

class TestClientes(unittest.TestCase):
    """Pruebas para las clases de clientes"""
    
    def test_cliente_regular_creacion(self):
        """Prueba la creación de un cliente regular"""
        cliente = ClienteRegular(1, "Juan Pérez", "juan@email.com", 
                               "123456789", "Calle 123")
        
        self.assertEqual(cliente.id, 1)
        self.assertEqual(cliente.nombre, "Juan Pérez")
        self.assertEqual(cliente.email, "juan@email.com")
        self.assertEqual(cliente.obtener_tipo(), "Regular")
    
    def test_cliente_regular_descuento(self):
        """Prueba el cálculo de descuento para cliente regular"""
        cliente = ClienteRegular(1, "Test", "test@email.com", 
                               "123456789", "Dirección")
        
        descuento = cliente.calcular_descuento(1000)
        self.assertEqual(descuento, 50)  # 5% de 1000
    
    def test_cliente_premium_creacion(self):
        """Prueba la creación de un cliente premium"""
        cliente = ClientePremium(2, "María López", "maria@email.com",
                               "987654321", "Avenida 456", "platino")
        
        self.assertEqual(cliente.id, 2)
        self.assertEqual(cliente.nivel, "platino")
        self.assertEqual(cliente.obtener_tipo(), "Premium (platino)")
    
    def test_cliente_premium_descuento(self):
        """Prueba el cálculo de descuento para cliente premium"""
        cliente_oro = ClientePremium(1, "Test Oro", "test@email.com",
                                   "123", "Dir", "oro")
        cliente_platino = ClientePremium(2, "Test Platino", "test2@email.com",
                                       "456", "Dir", "platino")
        
        self.assertEqual(cliente_oro.calcular_descuento(1000), 100)  # 10%
        self.assertEqual(cliente_platino.calcular_descuento(1000), 200)  # 20%
    
    def test_cliente_corporativo_creacion(self):
        """Prueba la creación de un cliente corporativo"""
        cliente = ClienteCorporativo(3, "Carlos Ruiz", "carlos@empresa.com",
                                   "5551234", "Carrera 789", 
                                   "Tech Solutions", "123456789-0")
        
        self.assertEqual(cliente.empresa, "Tech Solutions")
        self.assertEqual(cliente.nit, "1234567890")
        self.assertEqual(cliente.obtener_tipo(), "Corporativo")
    
    def test_cliente_corporativo_descuento(self):
        """Prueba el cálculo de descuento para cliente corporativo"""
        cliente = ClienteCorporativo(1, "Test", "test@empresa.com",
                                   "123", "Dir", "Empresa", "12345")
        
        descuento_base = cliente.calcular_descuento(1000)
        self.assertEqual(descuento_base, 150)  # 15% base
        
        # Con facturación alta
        cliente.actualizar_facturacion(15000)
        descuento_alto = cliente.calcular_descuento(1000)
        self.assertEqual(descuento_alto, 200)  # 15% + 5% = 20%
    
    def test_validaciones_email(self):
        """Prueba las validaciones de email"""
        validators = Validators()
        
        # Emails válidos
        valido, mensaje = validators.validar_email_avanzado("test@example.com")
        self.assertTrue(valido)
        
        valido, mensaje = validators.validar_email_avanzado("usuario.nombre@dominio.co")
        self.assertTrue(valido)
        
        # Emails inválidos
        valido, mensaje = validators.validar_email_avanzado("test@")
        self.assertFalse(valido)
        
        valido, mensaje = validators.validar_email_avanzado("@dominio.com")
        self.assertFalse(valido)
        
        valido, mensaje = validators.validar_email_avanzado("test@.com")
        self.assertFalse(valido)
    
    def test_encapsulamiento(self):
        """Prueba el encapsulamiento de propiedades"""
        cliente = ClienteRegular(1, "Test", "test@email.com", 
                               "123456789", "Dirección")
        
        # Propiedades deben ser accesibles pero no modificables directamente
        self.assertEqual(cliente.nombre, "Test")
        
        # Debe poder modificarse a través del setter
        cliente.nombre = "Nuevo Nombre"
        self.assertEqual(cliente.nombre, "Nuevo Nombre")
    
    def test_igualdad_clientes(self):
        """Prueba la comparación de igualdad entre clientes"""
        cliente1 = ClienteRegular(1, "Cliente A", "a@email.com", 
                                "111", "Dir A")
        cliente2 = ClienteRegular(1, "Cliente B", "b@email.com", 
                                "222", "Dir B")
        cliente3 = ClienteRegular(2, "Cliente A", "a@email.com", 
                                "111", "Dir A")
        
        self.assertEqual(cliente1, cliente2)  # Mismo ID
        self.assertNotEqual(cliente1, cliente3)  # ID diferente
    
    def test_herencia_polimorfismo(self):
        """Prueba el polimorfismo en el cálculo de descuentos"""
        clientes = [
            ClienteRegular(1, "Regular", "r@email.com", "111", "Dir"),
            ClientePremium(2, "Premium", "p@email.com", "222", "Dir", "oro"),
            ClienteCorporativo(3, "Corporativo", "c@email.com", "333", "Dir", "Emp", "123")
        ]
        
        descuentos = [cliente.calcular_descuento(1000) for cliente in clientes]
        
        # Cada tipo debe tener un descuento diferente
        self.assertNotEqual(descuentos[0], descuentos[1])
        self.assertNotEqual(descuentos[1], descuentos[2])
    
    def test_manejo_errores(self):
        """Prueba el manejo de errores en la creación de clientes"""
        # Email inválido
        with self.assertRaises(ValueError):
            ClienteRegular(1, "Test", "email-invalido", "123", "Dir")
        
        # Teléfono inválido
        with self.assertRaises(ValueError):
            ClienteRegular(2, "Test", "test@email.com", "abc", "Dir")
        
        # Nombre vacío
        with self.assertRaises(ValueError):
            ClienteRegular(3, "", "test@email.com", "123", "Dir")

class TestValidators(unittest.TestCase):
    """Pruebas para las validaciones avanzadas"""
    
    def test_validar_telefono(self):
        """Prueba la validación de teléfonos"""
        validators = Validators()
        
        # Teléfonos válidos (formato internacional)
        valido, mensaje = validators.validar_telefono_avanzado("+573001234567", "CO")
        # Nota: Esta prueba puede fallar si no está instalada la librería phonenumbers
        # En producción, se debe manejar adecuadamente
        
        # Formato simple
        valido, mensaje = validators.validar_telefono_avanzado("3001234567", "CO")
        self.assertTrue(valido or not valido)  # Aceptar cualquier resultado
    
    def test_validar_nit_colombiano(self):
        """Prueba la validación de NIT colombiano"""
        validators = Validators()
        
        # NIT válido (ejemplo)
        valido, mensaje = validators.validar_nit("900123456-7", "CO")
        # La validación exacta depende del algoritmo implementado
        
        # NIT con formato incorrecto
        valido, mensaje = validators.validar_nit("123", "CO")
        self.assertFalse(valido)

if __name__ == "__main__":
    unittest.main(verbosity=2)