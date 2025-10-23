# 🛒 Tienda - Sistema de Gestión de Ventas Online

Sistema completo de gestión de ventas online desarrollado en Python Flask. Permite administrar productos, clientes, ventas e inventario de manera eficiente.

## 🌟 Características

- **Gestión de Productos**: CRUD completo para productos con control de stock
- **Gestión de Clientes**: Administración de base de datos de clientes
- **Registro de Ventas**: Sistema completo de ventas con múltiples productos
- **Control de Inventario**: Actualización automática de stock al realizar ventas
- **Dashboard**: Panel de control con estadísticas y ventas recientes
- **Autenticación**: Sistema de login para proteger el acceso
- **Interfaz Intuitiva**: Diseño limpio y fácil de usar

## 📋 Requisitos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

## 🚀 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/gerojt/tienda.git
cd tienda
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Iniciar la aplicación:
```bash
python app.py
```

4. Abrir el navegador en: http://127.0.0.1:5000

## 🔑 Credenciales por Defecto

- **Usuario**: admin
- **Contraseña**: admin

⚠️ **Nota**: Cambiar estas credenciales en producción.

## 📱 Uso del Sistema

### Dashboard
- Vista general con estadísticas del negocio
- Total de productos, clientes y ventas
- Ingresos totales
- Ventas recientes

### Gestión de Productos
- Agregar nuevos productos con nombre, descripción, precio y stock
- Editar información de productos existentes
- Eliminar productos
- Ver lista completa de productos

### Gestión de Clientes
- Registrar nuevos clientes con datos de contacto
- Actualizar información de clientes
- Eliminar clientes
- Ver lista completa de clientes

### Registro de Ventas
- Crear nueva venta seleccionando cliente y productos
- Añadir múltiples productos a una venta
- Validación automática de stock disponible
- Actualización automática de inventario
- Ver detalle completo de cada venta
- Eliminar ventas (restaura el stock)

## 🗄️ Estructura de la Base de Datos

### Productos (Product)
- id: Identificador único
- name: Nombre del producto
- description: Descripción detallada
- price: Precio unitario
- stock: Cantidad disponible
- created_at: Fecha de creación

### Clientes (Customer)
- id: Identificador único
- name: Nombre del cliente
- email: Correo electrónico (único)
- phone: Teléfono
- address: Dirección
- created_at: Fecha de registro

### Ventas (Sale)
- id: Identificador único
- customer_id: Referencia al cliente
- total: Monto total de la venta
- status: Estado de la venta
- created_at: Fecha de la venta

### Items de Venta (SaleItem)
- id: Identificador único
- sale_id: Referencia a la venta
- product_id: Referencia al producto
- quantity: Cantidad vendida
- price: Precio al momento de la venta

## 🛠️ Tecnologías Utilizadas

- **Flask**: Framework web para Python
- **SQLAlchemy**: ORM para gestión de base de datos
- **SQLite**: Base de datos integrada
- **HTML/CSS**: Interfaz de usuario
- **JavaScript**: Funcionalidad del lado del cliente

## 📂 Estructura del Proyecto

```
tienda/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias del proyecto
├── README.md             # Documentación
├── .gitignore           # Archivos ignorados por git
├── templates/           # Plantillas HTML
│   ├── base.html       # Plantilla base
│   ├── index.html      # Página de inicio
│   ├── login.html      # Página de login
│   ├── dashboard.html  # Dashboard principal
│   ├── products.html   # Lista de productos
│   ├── product_form.html  # Formulario de producto
│   ├── customers.html  # Lista de clientes
│   ├── customer_form.html # Formulario de cliente
│   ├── sales.html      # Lista de ventas
│   ├── sale_form.html  # Formulario de venta
│   └── sale_detail.html   # Detalle de venta
└── tienda.db           # Base de datos SQLite (se crea automáticamente)
```

## 🔐 Seguridad

- Sistema de autenticación básico
- Sesiones para mantener estado de login
- Validación de datos en formularios
- Protección de rutas mediante decorador @login_required

⚠️ **Para producción**:
- Implementar hashing de contraseñas (bcrypt, argon2)
- Cambiar SECRET_KEY
- Usar base de datos más robusta (PostgreSQL, MySQL)
- Implementar HTTPS
- Añadir validación CSRF

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso libre.

## 📧 Contacto

Para preguntas o sugerencias, por favor abre un issue en el repositorio.
