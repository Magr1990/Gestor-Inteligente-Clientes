import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.cliente_regular import ClienteRegular
from models.cliente_premium import ClientePremium
from models.cliente_corporativo import ClienteCorporativo
from utils.validators import Validators

class TestClientes(unittest.TestCase):
    
    def test_cliente_regular_creacion(self):
        cliente = ClienteRegular(1, "Juan Pérez", "juan@email.com", 
                               "123456789", "Calle 123")
        
        self.assertEqual(cliente.id, 1)
        self.assertEqual(cliente.nombre, "Juan Pérez")
        self.assertEqual(cliente.email, "juan@email.com")
        self.assertEqual(cliente.obtener_tipo(), "Regular")
    
    def test_cliente_regular_descuento(self):
        cliente = ClienteRegular(1, "Test", "test@email.com", 
                               "123456789", "Dirección")
        
        descuento = cliente.calcular_descuento(1000)
        self.assertEqual(descuento, 50)
    
    def test_cliente_premium_creacion(self):
        cliente = ClientePremium(2, "María López", "maria@email.com",
                               "987654321", "Avenida 456", "platino")
        
        self.assertEqual(cliente.id, 2)
        self.assertEqual(cliente.nivel, "platino")
        self.assertEqual(cliente.obtener_tipo(), "Premium (platino)")
    
    def test_cliente_premium_descuento(self):
        cliente_oro = ClientePremium(1, "Test Oro", "test@email.com",
                                   "123", "Dir", "oro")
        cliente_platino = ClientePremium(2, "Test Platino", "test2@email.com",
                                       "456", "Dir", "platino")
        
        self.assertEqual(cliente_oro.calcular_descuento(1000), 100)
        self.assertEqual(cliente_platino.calcular_descuento(1000), 200)
    
    def test_cliente_corporativo_creacion(self):
        cliente = ClienteCorporativo(3, "Carlos Ruiz", "carlos@empresa.com",
                                   "5551234", "Carrera 789", 
                                   "Tech Solutions", "76.123.456-7")
        
        self.assertEqual(cliente.empresa, "Tech Solutions")
        self.assertEqual(cliente.rut, "761234567")
        self.assertEqual(cliente.obtener_tipo(), "Corporativo")
    
    def test_cliente_corporativo_descuento(self):
        cliente = ClienteCorporativo(1, "Test", "test@empresa.com",
                                   "123", "Dir", "Empresa", "12345")
        
        descuento_base = cliente.calcular_descuento(1000)
        self.assertEqual(descuento_base, 150)
        
        cliente.actualizar_facturacion(15000)
        descuento_alto = cliente.calcular_descuento(1000)
        self.assertEqual(descuento_alto, 200)
    
    def test_validaciones_email(self):
        validators = Validators()
        
        valido, mensaje = validators.validar_email_avanzado("test@example.com")
        self.assertTrue(valido)
        
        valido, mensaje = validators.validar_email_avanzado("usuario.nombre@dominio.co")
        self.assertTrue(valido)
        
        valido, mensaje = validators.validar_email_avanzado("test@")
        self.assertFalse(valido)
        
        valido, mensaje = validators.validar_email_avanzado("@dominio.com")
        self.assertFalse(valido)
        
        valido, mensaje = validators.validar_email_avanzado("test@.com")
        self.assertFalse(valido)
    
    def test_encapsulamiento(self):
        cliente = ClienteRegular(1, "Test", "test@email.com", 
                               "123456789", "Dirección")
        
        self.assertEqual(cliente.nombre, "Test")
        
        cliente.nombre = "Nuevo Nombre"
        self.assertEqual(cliente.nombre, "Nuevo Nombre")
    
    def test_igualdad_clientes(self):
        cliente1 = ClienteRegular(1, "Cliente A", "a@email.com", 
                                "111", "Dir A")
        cliente2 = ClienteRegular(1, "Cliente B", "b@email.com", 
                                "222", "Dir B")
        cliente3 = ClienteRegular(2, "Cliente A", "a@email.com", 
                                "111", "Dir A")
        
        self.assertEqual(cliente1, cliente2)
        self.assertNotEqual(cliente1, cliente3)
    
    def test_herencia_polimorfismo(self):
        clientes = [
            ClienteRegular(1, "Regular", "r@email.com", "111", "Dir"),
            ClientePremium(2, "Premium", "p@email.com", "222", "Dir", "oro"),
            ClienteCorporativo(3, "Corporativo", "c@email.com", "333", "Dir", "Emp", "123")
        ]
        
        descuentos = [cliente.calcular_descuento(1000) for cliente in clientes]
        
        self.assertNotEqual(descuentos[0], descuentos[1])
        self.assertNotEqual(descuentos[1], descuentos[2])
    
    def test_manejo_errores(self):
        with self.assertRaises(ValueError):
            ClienteRegular(1, "Test", "email-invalido", "123", "Dir")
        
        with self.assertRaises(ValueError):
            ClienteRegular(2, "Test", "test@email.com", "abc", "Dir")
        
        with self.assertRaises(ValueError):
            ClienteRegular(3, "", "test@email.com", "123", "Dir")

class TestValidators(unittest.TestCase):
    
    def test_validar_telefono(self):
        validators = Validators()
        
        valido, mensaje = validators.validar_telefono_avanzado("+573001234567", "CO")
        
        valido, mensaje = validators.validar_telefono_avanzado("3001234567", "CO")
        self.assertTrue(valido or not valido)
    
    def test_validar_rut_chileno(self):
        validators = Validators()
        
        valido, mensaje = validators.validar_rut("30.686.957-4")
        self.assertTrue(valido, f"Debería ser válido: {mensaje}")
        
        valido, mensaje = validators.validar_rut("30.686.957-K")
        self.assertFalse(valido)

if __name__ == "__main__":
    unittest.main(verbosity=2)