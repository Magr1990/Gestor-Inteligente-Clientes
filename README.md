# Gestor Inteligente de Clientes (GIC)

Sistema integral de gestión de clientes desarrollado en Python para la empresa **SolutionTech**. Este proyecto implementa una solución escalable basada en Programación Orientada a Objetos (POO), con interfaz gráfica, persistencia de datos y validaciones avanzadas.

## 🚀 Características

- **Gestión de Clientes**: CRUD completo (Crear, Leer, Actualizar, Eliminar).
- **Tipos de Clientes**: Soporte para clientes Regulares, Premium y Corporativos con lógica de negocio diferenciada (polimorfismo).
- **Interfaz Gráfica**: GUI moderna construida con **Tkinter**.
- **Persistencia de Datos**:
  - Base de datos **SQLite** para almacenamiento robusto.
  - Exportación e importación en formatos **JSON** y **CSV**.
- **Validaciones Avanzadas**: Verificación de emails, teléfonos (formato internacional) y NIT.
- **Sistema de Logs**: Registro detallado de operaciones y errores.
- **Integraciones**: Simulación de servicios de notificación por email y validación externa.

## 📋 Requisitos

- Python 3.8 o superior
- Librerías externas: `phonenumbers`, `requests`

## 🛠️ Instalación y Ejecución

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/Magr1990/Gestor-Inteligente-Clientes.git
   cd Gestor-Inteligente-Clientes
   ```

2. **Instalar dependencias**:
   ```bash
   pip install phonenumbers requests
   ```

3. **Organizar estructura**:
   El proyecto incluye un script para asegurar que los módulos estén en su lugar.
   ```bash
   python organize.py
   ```

4. **Ejecutar la aplicación**:
   ```bash
   python main.py
   ```

## 📂 Estructura del Proyecto

- `gui/`: Interfaz gráfica (Ventana principal, formularios).
- `models/`: Clases de negocio (Cliente, ClientePremium, etc.).
- `database/`: Gestión de SQLite y archivos JSON/CSV.
- `utils/`: Validadores y sistema de logs.
- `api_integrations/`: Servicios externos simulados.
- `tests/`: Pruebas unitarias.

## 👤 Autor

Proyecto desarrollado como parte del módulo de evaluación de Python Avanzado.