# Gestor Inteligente de Clientes (GIC)

Sistema completo de gestión de clientes para SolutionTech, desarrollado en Python con POO.

## Características Principales

### ✅ POO Completo
- **Herencia**: Cliente base con 3 tipos especializados
- **Polimorfismo**: Métodos comunes con comportamientos diferentes
- **Encapsulación**: Atributos privados con getters/setters
- **Abstracción**: Clases abstractas y métodos abstractos

### ✅ Tipos de Clientes
1. **Cliente Regular**: Descuento básico (5%) + sistema de puntos
2. **Cliente Premium**: Descuentos mayores (10-20%) según nivel
3. **Cliente Corporativo**: Descuentos corporativos + facturación empresarial

### ✅ Validaciones Avanzadas
- Email con regex y verificación de dominio
- Teléfono internacional con phonenumbers
- NIT con algoritmo de verificación
- Dirección con validación de componentes
- Manejo de excepciones personalizadas

### ✅ Persistencia de Datos
- **SQLite**: Base de datos relacional para operaciones CRUD
- **JSON**: Exportación/importación y backups
- **CSV**: Compatibilidad con otras aplicaciones

### ✅ Interfaz Gráfica (Tkinter)
- Gestión completa de clientes (CRUD)
- Búsqueda avanzada
- Validación en tiempo real
- Sistema de logs integrado
- Exportación/importación de datos

### ✅ Integraciones con APIs
- Validación de emails (simulada)
- Envío de emails de bienvenida
- Sistema de notificaciones
- APIs extensibles para servicios externos

### ✅ Sistema de Logging
- Registro de todas las operaciones
- Niveles de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Rotación automática de archivos
- Backup de logs

## Instalación y Ejecución

### 1. Requisitos Previos
```bash
Python 3.8 o superior