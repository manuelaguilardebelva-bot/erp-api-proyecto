# ERP API Project

Este proyecto es el backend (API REST) para un sistema ERP, construido con **FastAPI** y **Python**. Ha sido estructurado siguiendo las mejores prácticas para aplicaciones asíncronas, utilizando inyección de dependencias, el patrón repositorio y separación de responsabilidades en diferentes capas (Modelos, Esquemas, Repositorios, Servicios y Controladores/Rutas).

## Características

- ⚡️ **FastAPI** para endpoints de alto rendimiento.
- 🗄️ **SQLAlchemy (Async)** como ORM, empleando `asyncpg` para conexiones a bases de datos PostgreSQL de forma no bloqueante.
- 🏗️ **Patrón Repositorio y Capa de Servicios**, que facilita el testing y el mantenimiento del código.
- ⚙️ **Configuración centralizada**, gestionada mediante `pydantic-settings` y variables de entorno (`.env`).
- 📝 **Estructura modular y escalable** organizada funcionalmente.

## Estructura del Proyecto

```text
erp-api-proyecto/
├── app/
│   ├── api/                  # Rutas y controladores de la API
│   │   └── v1/
│   │       ├── endpoints/    # Endpoints específicos (ej. timesheets.py)
│   │       └── router.py     # Router principal de la versión 1
│   ├── core/                 # Configuraciones core (DB, environment, security)
│   │   ├── config.py
│   │   └── database.py
│   ├── models/               # Modelos SQLAlchemy (Tablas en Base de Datos)
│   ├── repositories/         # Capa de Acceso a Datos (Consultas SQL/ORM)
│   ├── schemas/              # Modelos Pydantic (Validación de Request/Response)
│   ├── services/             # Lógica de Negocio (Business logic)
│   └── main.py               # Punto de entrada de la aplicación FastAPI
├── requirements.txt          # Dependencias de Python
└── README.md                 # Documentación principal
```

## Requisitos Previos

- Python 3.10 o superior.
- Una base de datos PostgreSQL.

## Configuración y Despliegue Local

1. **Clonar el repositorio:**

   ```bash
   git clone <url-del-repositorio>
   cd erp-api-proyecto
   ```

2. **Crear y activar un entorno virtual (recomendado):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar las variables de entorno:**

   Crea un archivo `.env` en la raíz del proyecto y define la cadena de conexión a tu base de datos:

   ```env
   DATABASE_URL=postgresql://usuario:contraseña@servidor:puerto/nombre_base_datos
   ```

   > **Nota:** La aplicación convertirá automáticamente las cadenas `postgres://` o `postgresql://` para usar el driver asíncrono `postgresql+asyncpg://` internamente.

## Ejecución del Servidor

Para iniciar el servidor de desarrollo utilizando Uvicorn, ejecuta:

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en [http://localhost:8000](http://localhost:8000).

Puedes acceder a la documentación interactiva generada automáticamente por FastAPI (Swagger UI) en:

👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

## Endpoints Principales

Actualmente el sistema soporta el registro de fichajes, horas de los trabajadores y un sistema de logs automáticos:

- `POST /api/v1/timesheets/clock-out/{usuario_id}`: Detiene o cierra la jornada actual de un usuario dado, calcula automáticamente los minutos productivos y guarda un log de la acción de manera asíncrona en la base de datos.
