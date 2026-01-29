"""
Cliente Corporativo - Subclase de Cliente
"""

from models.cliente import Cliente

class ClienteCorporativo(Cliente):
    """Cliente Corporativo para empresas"""
    
    def __init__(self, id_cliente, nombre, email, telefono, direccion, 
                 empresa, nit, contacto_alterno=None, fecha_registro=None):
        super().__init__(id_cliente, nombre, email, telefono, direccion, fecha_registro)
        self._empresa = self._validar_empresa(empresa)
        self._nit = self._validar_nit(nit)
        self._contacto_alterno = contacto_alterno
        self._facturacion_mensual = 0
    
    def _validar_empresa(self, empresa):
        """Valida el nombre de la empresa"""
        if not empresa or not empresa.strip():
            raise ValueError("El nombre de la empresa no puede estar vacío")
        return empresa.strip()
    
    def _validar_nit(self, nit):
        """Valida el NIT de la empresa"""
        if not nit or not str(nit).strip():
            raise ValueError("El NIT no puede estar vacío")
        # Validación básica de NIT (puede mejorarse según país)
        nit_str = str(nit).replace('-', '').replace('.', '').strip()
        if not nit_str.isdigit():
            raise ValueError("El NIT debe contener solo números")
        return nit_str
    
    def calcular_descuento(self, monto):
        """Calcula descuento corporativo (15% base + bonificación por volumen)"""
        descuento_base = 0.15
        
        # Bonificación por volumen de facturación
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
        """Actualiza el monto de facturación mensual"""
        if monto >= 0:
            self._facturacion_mensual = monto
    
    @property
    def empresa(self):
        return self._empresa
    
    @property
    def nit(self):
        return self._nit
    
    @property
    def contacto_alterno(self):
        return self._contacto_alterno
    
    @property
    def facturacion_mensual(self):
        return self._facturacion_mensual