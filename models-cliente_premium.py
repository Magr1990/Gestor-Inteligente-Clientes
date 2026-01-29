from models.cliente import Cliente

class ClientePremium(Cliente):
    
    def __init__(self, id_cliente, nombre, email, telefono, direccion, rut,
                 nivel="oro", fecha_registro=None):
        super().__init__(id_cliente, nombre, email, telefono, direccion, rut, fecha_registro)
        self._nivel = self._validar_nivel(nivel)
        self._beneficios_extra = []
    
    def _validar_nivel(self, nivel):
        niveles_validos = ["oro", "plata", "platino"]
        if nivel.lower() not in niveles_validos:
            raise ValueError(f"Nivel debe ser uno de: {', '.join(niveles_validos)}")
        return nivel.lower()
    
    def calcular_descuento(self, monto):
        descuentos = {
            "oro": 0.10,
            "plata": 0.15,
            "platino": 0.20
        }
        return monto * descuentos.get(self._nivel, 0.10)
    
    def obtener_tipo(self):
        return f"Premium ({self._nivel})"
    
    def agregar_beneficio(self, beneficio):
        if beneficio not in self._beneficios_extra:
            self._beneficios_extra.append(beneficio)
    
    @property
    def nivel(self):
        return self._nivel
    
    @property
    def beneficios_extra(self):
        return self._beneficios_extra.copy()