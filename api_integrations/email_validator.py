"""
Integración con API de validación de emails
"""

import requests
import re
from abc import ABC, abstractmethod

class EmailValidator(ABC):
    """Clase abstracta para validación de emails"""
    
    @abstractmethod
    def validar_email(self, email):
        pass

class SimpleEmailValidator(EmailValidator):
    """Validador simple de emails (sin API real)"""
    
    def validar_email(self, email):
        """Valida el formato y dominio del email"""
        try:
            # Validación básica de formato
            patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(patron, email):
                return {
                    'valido': False,
                    'mensaje': 'Formato de email inválido',
                    'detalles': {}
                }
            
            # Simular validación de dominio
            dominio = email.split('@')[1]
            dominios_populares = ['gmail.com', 'hotmail.com', 'yahoo.com', 'outlook.com']
            
            if dominio in dominios_populares:
                return {
                    'valido': True,
                    'mensaje': 'Email válido',
                    'detalles': {
                        'dominio': dominio,
                        'es_popular': True
                    }
                }
            else:
                # Simular verificación de dominio
                return {
                    'valido': True,
                    'mensaje': 'Email válido (dominio verificado)',
                    'detalles': {
                        'dominio': dominio,
                        'es_popular': False,
                        'advertencia': 'Verificar manualmente dominio no común'
                    }
                }
                
        except Exception as e:
            return {
                'valido': False,
                'mensaje': f'Error en validación: {str(e)}',
                'detalles': {}
            }

class APIBasedEmailValidator(EmailValidator):
    """Validador de emails con API externa (simulada)"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "https://api.emailvalidator.com/v1/"  # URL simulada
    
    def validar_email(self, email):
        """Valida email usando API externa (simulación)"""
        try:
            # En una implementación real, aquí haríamos una petición HTTP
            # Por ahora simulamos la respuesta
            
            # Simular diferentes casos
            if 'test' in email or 'fake' in email:
                return {
                    'valido': False,
                    'mensaje': 'Email detectado como temporal/falso',
                    'detalles': {
                        'score': 0.1,
                        'disposable': True,
                        'risk_level': 'high'
                    }
                }
            elif 'gmail.com' in email or 'hotmail.com' in email:
                return {
                    'valido': True,
                    'mensaje': 'Email válido y seguro',
                    'detalles': {
                        'score': 0.9,
                        'disposable': False,
                        'risk_level': 'low',
                        'deliverable': True
                    }
                }
            else:
                return {
                    'valido': True,
                    'mensaje': 'Email válido',
                    'detalles': {
                        'score': 0.7,
                        'disposable': False,
                        'risk_level': 'medium',
                        'deliverable': True
                    }
                }
                
        except Exception as e:
            return {
                'valido': False,
                'mensaje': f'Error en API: {str(e)}',
                'detalles': {}
            }