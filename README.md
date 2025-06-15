# Proyecto Flask: Gestor de Tareas

## Descripción
Aplicación web desarrollada con Flask para la gestión de tareas, diseñada con principios de escalabilidad, mantenibilidad y bajo acoplamiento. Incluye validación de datos con Pydantic, pruebas automatizadas con pytest y arquitectura preparada para migración a MySQL.

## Instrucciones de instalación
1. Clona el repositorio y accede a la carpeta del proyecto.
2. Crea y activa un entorno virtual:
   ```pwsh
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Instala las dependencias:
   ```pwsh
   pip install -r requirements.txt
   ```

## Instrucciones de uso
1. Ejecuta la aplicación:
   ```pwsh
   python run.py
   ```
2. Accede a la API en `http://localhost:5000`.

## Estructura del proyecto
```
proyecto/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models/
│   │   └── task.py
│   ├── schemas/
│   │   └── task_schema.py
│   ├── services/
│   │   └── task_manager.py
│   ├── repositories/
│   │   ├── i_task_repository.py
│   │   └── json_task_repository.py
│   ├── data/
│   │   └── tasks.json
├── tests/
│   └── test_tasks.py
├── requirements.txt
├── run.py
└── README.md
```

## Ejemplos de uso de la API
- **Obtener todas las tareas:**
  ```http
  GET /tasks
  ```
- **Obtener una tarea por ID:**
  ```http
  GET /tasks/1
  ```
- **Crear una tarea:**
  ```http
  POST /tasks
  Content-Type: application/json
  {
    "id": 1,
    "title": "Tarea de ejemplo",
    "description": "Descripción",
    "priority": "media",
    "effort_hours": 2.5,
    "status": "pendiente",
    "assigned_to": "Carlos"
  }
  ```
- **Actualizar una tarea:**
  ```http
  PUT /tasks/1
  Content-Type: application/json
  {
    "id": 1,
    "title": "Tarea actualizada",
    "description": "Nueva descripción",
    "priority": "alta",
    "effort_hours": 3.0,
    "status": "en progreso",
    "assigned_to": "Ana"
  }
  ```
- **Eliminar una tarea:**
  ```http
  DELETE /tasks/1
  ```

## Dependencias y requisitos
- Python >= 3.8
- Flask
- Pydantic
- pytest
- flask-cors
- python-dotenv
- (Opcional para migración) SQLAlchemy, PyMySQL

## Información sobre las pruebas automatizadas
Las pruebas unitarias están en `tests/test_tasks.py` y se ejecutan con:
```pwsh
pytest -s
```
Las pruebas cubren creación, lectura, actualización, eliminación y manejo de errores.

## Información sobre la migración futura a MySQL
La arquitectura desacoplada permite sustituir fácilmente el repositorio JSON por uno basado en MySQL implementando la interfaz `ITaskRepository`. Solo será necesario crear un nuevo repositorio (por ejemplo, `MySQLTaskRepository`) y pasarlo a `TaskManager`.

## Licencia
MIT License

## Contacto
Carlos Hernández — carlos@laorotava.org
