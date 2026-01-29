"""
Utilidades de validación avanzada
"""

import re
try:
    import phonenumbers
    # Si ves un error aquí, necesitas instalar la librería: pip install phonenumbers
except ImportError:
    phonenumbers = None
from datetime import datetime

class Validators:
    """Clase con métodos de validación avanzada"""
    
    @staticmethod
    def validar_email_avanzado(email):
        """Validación avanzada de email"""
        try:
            # Validación básica con regex
            patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(patron, email):
                return False, "Formato de email inválido"
            
            # Validar longitud
            if len(email) > 254:
                return False, "Email demasiado largo"
            
            # Validar partes del email
            local_part, domain = email.split('@')
            
            if len(local_part) > 64:
                return False, "Parte local del email demasiado larga"
            
            # Validar dominio
            if domain.startswith('.') or domain.endswith('.'):
                return False, "Dominio inválido"
            
            # Validar que no haya caracteres especiales problemáticos
            if re.search(r'[\.]{2,}', local_part):
                return False, "Puntos consecutivos no permitidos"
            
            if local_part.startswith('.') or local_part.endswith('.'):
                return False, "La parte local no puede empezar o terminar con punto"
            
            return True, "Email válido"
            
        except Exception as e:
            return False, f"Error en validación: {str(e)}"
    
    @staticmethod
    def validar_telefono_avanzado(telefono, pais="CO"):
        """Validación avanzada de teléfono usando phonenumbers"""
        if phonenumbers:
            try:
                numero = phonenumbers.parse(telefono, pais)
                
                if not phonenumbers.is_valid_number(numero):
                    return False, "Número de teléfono inválido"
                
                if not phonenumbers.is_possible_number(numero):
                    return False, "Número de teléfono imposible"
                
                # Formatear a formato internacional
                formato_internacional = phonenumbers.format_number(
                    numero, 
                    phonenumbers.PhoneNumberFormat.INTERNATIONAL
                )
                
                return True, formato_internacional
                
            except phonenumbers.phonenumberutil.NumberParseException:
                pass # Fallback a validación simple
            
        # Fallback a validación simple
        telefono_limpio = re.sub(r'[^\d+]', '', telefono)
        
        if len(telefono_limpio) < 8:
            return False, "Teléfono demasiado corto"
        
        if len(telefono_limpio) > 15:
            return False, "Teléfono demasiado largo"
        
        if not telefono_limpio.startswith('+'):
            return False, "Formato internacional requerido (+)"
        
        return True, telefono_limpio
    
    @staticmethod
    def validar_nit(nit, pais="CO"):
        """Validación de NIT según país"""
        try:
            nit_limpio = re.sub(r'[^\d]', '', str(nit))
            
            if pais == "CO":  # Colombia
                if len(nit_limpio) < 8 or len(nit_limpio) > 12:
                    return False, "NIT colombiano debe tener 8-12 dígitos"
                
                # Algoritmo de verificación para Colombia
                multiplicadores = [3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53]
                nit_sin_dv = nit_limpio[:-1]
                digito_verificador = int(nit_limpio[-1])
                
                suma = 0
                for i, digito in enumerate(reversed(nit_sin_dv)):
                    suma += int(digito) * multiplicadores[i]
                
                residuo = suma % 11
                if residuo >= 2:
                    resultado = 11 - residuo
                else:
                    resultado = residuo
                
                if resultado == digito_verificador:
                    return True, f"NIT válido: {nit_limpio}"
                else:
                    return False, "Dígito verificador inválido"
            
            else:
                # Validación básica para otros países
                if len(nit_limpio) < 5:
                    return False, "NIT demasiado corto"
                
                if not nit_limpio.isdigit():
                    return False, "NIT debe contener solo números"
                
                return True, f"NIT válido: {nit_limpio}"
                
        except Exception as e:
            return False, f"Error en validación NIT: {str(e)}"
    
    @staticmethod
    def validar_direccion_completa(direccion):
        """Validación avanzada de dirección"""
        try:
            direccion_limpia = direccion.strip()
            
            if len(direccion_limpia) < 10:
                return False, "Dirección demasiado corta"
            
            if len(direccion_limpia) > 200:
                return False, "Dirección demasiado larga"
            
            # Verificar que tenga componentes básicos
            componentes_minimos = 2
            palabras = direccion_limpia.split()
            
            if len(palabras) < componentes_minimos:
                return False, "Dirección incompleta"
            
            # Verificar que tenga números (opcional pero común)
            if not any(char.isdigit() for char in direccion_limpia):
                print("Advertencia: Dirección sin número")
            
            return True, "Dirección válida"
            
        except Exception as e:
            return False, f"Error en validación de dirección: {str(e)}"
    
    @staticmethod
    def validar_fecha_nacimiento(fecha_str, formato="%Y-%m-%d", edad_minima=18):
        """Validación de fecha de nacimiento"""
        try:
            fecha = datetime.strptime(fecha_str, formato)
            hoy = datetime.now()
            
            # Calcular edad
            edad = hoy.year - fecha.year
            if (hoy.month, hoy.day) < (fecha.month, fecha.day):
                edad -= 1
            
            if edad < edad_minima:
                return False, f"Edad mínima requerida: {edad_minima} años"
            
            if edad > 120:
                return False, "Fecha de nacimiento inválida"
            
            return True, f"Fecha válida, edad: {edad} años"
            
        except ValueError:
            return False, f"Formato de fecha inválido. Use: {formato}"
        except Exception as e:
            return False, f"Error en validación de fecha: {str(e)}"