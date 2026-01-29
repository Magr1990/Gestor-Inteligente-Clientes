from models.cliente import Cliente

class ClienteCorporativo(Cliente):
    
    def __init__(self, id_cliente, nombre, email, telefono, direccion, 
                 empresa, rut, contacto_alterno=None, fecha_registro=None):
        super().__init__(id_cliente, nombre, email, telefono, direccion, rut, fecha_registro)
        self._empresa = self._validar_empresa(empresa)
        self._contacto_alterno = contacto_alterno
        self._facturacion_mensual = 0
    
    def _validar_empresa(self, empresa):
        if not empresa or not empresa.strip():
            raise ValueError("El nombre de la empresa no puede estar vacío")
        return empresa.strip()
    
    def calcular_descuento(self, monto):
        descuento_base = 0.15
        
        if self._facturacion_mensual > 10000:
            descuento_extra = 0.05
        elif self._facturacion_mensual > 5000:
            descuento_extra = 0.03
        else:
            descuento_extra = 0
        
        return monto * (descuento_base + descuento_extra)
    
    def obtener_tipo(self):
        return "Corporativo"
    
    def actualizar_facturacion(self, monto):
        if monto >= 0:
            self._facturacion_mensual = monto
    
    @property
    def empresa(self):
        return self._empresa
    
    @property
    def contacto_alterno(self):
        return self._contacto_alterno
    
    @property
    def facturacion_mensual(self):
        return self._facturacion_mensual