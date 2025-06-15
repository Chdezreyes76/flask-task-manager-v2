# Proyecto Flask: Gestor de Tareas + Integración IA (Entregable 2)

## Descripción
Aplicación web desarrollada con Flask para la gestión de tareas, diseñada con principios de escalabilidad, mantenibilidad y bajo acoplamiento. Incluye integración con OpenAI para generación automática de descripciones, categorización, estimación de esfuerzo y análisis de riesgos, así como monitoreo de tokens consumidos por tarea.

## Novedades Entregable 2: Integración con IA
- **Nuevos campos en el modelo Task:**
  - `category`: categoría de la tarea (Frontend, Backend, etc.)
  - `risk_analysis`: análisis de riesgos generado por IA
  - `risk_mitigation`: plan de mitigación generado por IA
  - `token_usage`: tokens acumulados consumidos por la tarea
- **Nuevos endpoints de IA:**
  - `POST /ai/tasks/describe/<id>`: genera la descripción de la tarea
  - `POST /ai/tasks/categorize/<id>`: clasifica la tarea por categoría
  - `POST /ai/tasks/estimate/<id>`: estima el esfuerzo en horas
  - `POST /ai/tasks/audit/<id>`: genera análisis de riesgos y plan de mitigación
- **Monitoreo de tokens:**
  - Cada operación de IA suma los tokens consumidos al campo `token_usage` de la tarea
- **Configuración sencilla de OpenAI vía `.env`**

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

## Configuración de OpenAI
1. Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
   ```env
   OPENAI_API_KEY=tu_api_key_de_openai
   ```
2. (Opcional) Puedes configurar otros parámetros como modelo, temperatura, etc.

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
│   ├── routes/
│   │   ├── routes.py
│   │   └── ai_routes.py
│   ├── models/
│   │   └── task.py
│   ├── schemas/
│   │   └── task_schema.py
│   ├── services/
│   │   ├── task_manager.py
│   │   └── ai_task_manager.py
│   ├── repositories/
│   │   ├── i_task_repository.py
│   │   └── json_task_repository.py
│   ├── data/
│   │   └── tasks.json
├── tests/
│   ├── test_tasks.py
│   └── test_ai_endpoints.py
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

### Endpoints de IA (OpenAI)
- **Generar descripción:**
  ```http
  POST /ai/tasks/describe/1
  ```
  Respuesta:
  ```json
  {
    "id": 1,
    "title": "...",
    "description": "Descripción generada por IA",
    ...
    "token_usage": 123
  }
  ```
- **Clasificar tarea:**
  ```http
  POST /ai/tasks/categorize/1
  ```
  Respuesta:
  ```json
  {
    "id": 1,
    "category": "Backend",
    ...
    "token_usage": 150
  }
  ```
- **Estimar esfuerzo:**
  ```http
  POST /ai/tasks/estimate/1
  ```
  Respuesta:
  ```json
  {
    "id": 1,
    "effort_hours": 8,
    ...
    "token_usage": 180
  }
  ```
- **Auditoría de riesgos:**
  ```http
  POST /ai/tasks/audit/1
  ```
  Respuesta:
  ```json
  {
    "id": 1,
    "risk_analysis": "...",
    "risk_mitigation": "...",
    ...
    "token_usage": 250
  }
  ```

## Dependencias y requisitos
- Python >= 3.8
- Flask
- Pydantic
- pytest
- flask-cors
- python-dotenv
- openai
- tiktoken

## Información sobre las pruebas automatizadas
Las pruebas unitarias están en `tests/test_tasks.py` y las de integración de IA en `tests/test_ai_endpoints.py`:
```pwsh
pytest tests/test_tasks.py
pytest tests/test_ai_endpoints.py
```
Las pruebas cubren creación, lectura, actualización, eliminación, manejo de errores y operaciones de IA (incluyendo acumulación de tokens).

## Información sobre la migración futura a MySQL
La arquitectura desacoplada permite sustituir fácilmente el repositorio JSON por uno basado en MySQL implementando la interfaz `ITaskRepository`. Solo será necesario crear un nuevo repositorio (por ejemplo, `MySQLTaskRepository`) y pasarlo a `TaskManager`.

## Licencia
MIT License

## Contacto
Carlos Hernández — carlos@laorotava.org

## Cuaderno de pruebas Jupyter

Se incluye el cuaderno `entregable2_test_cuaderno.ipynb` en la raíz del proyecto, que permite probar de forma interactiva y guiada todas las funcionalidades del backend, incluyendo:

- Creación de tareas básicas.
- Enriquecimiento de tareas con IA (descripción, categorización, estimación de esfuerzo, auditoría).
- Extracción y visualización de tokens consumidos.
- Pruebas de endpoints y validaciones.
- Descarga de resultados enriquecidos.

**¿Cómo usarlo?**
1. Activa el entorno virtual y lanza Jupyter Notebook o VS Code.
2. Abre el archivo `entregable2_test_cuaderno.ipynb`.
3. Ejecuta las celdas en orden para comprobar y validar toda la integración del sistema.
