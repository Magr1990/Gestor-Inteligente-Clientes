from models.cliente import Cliente

class ClienteRegular(Cliente):
    
    def __init__(self, id_cliente, nombre, email, telefono, direccion, rut,
                 puntos_fidelidad=0, fecha_registro=None):
        super().__init__(id_cliente, nombre, email, telefono, direccion, rut, fecha_registro)
        self._puntos_fidelidad = max(0, puntos_fidelidad)
    
    def calcular_descuento(self, monto):
        return monto * 0.05
    
    def obtener_tipo(self):
        return "Regular"
    
    def agregar_puntos(self, puntos):
        if puntos > 0:
            self._puntos_fidelidad += puntos
    
    def canjear_puntos(self, puntos):
        if puntos <= self._puntos_fidelidad:
            self._puntos_fidelidad -= puntos
            return True
        return False
    
    @property
    def puntos_fidelidad(self):
        return self._puntos_fidelidad