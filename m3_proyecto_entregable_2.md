
Entregable 2: API REST en Flask o FastAPI con openai sdk

Sobre el proyecto entregable 1, añadir openai sdk a Flask o FastAPI y para lograr generar descripciones de tareas introducidas por el usuario y registrar el número de tokens consumidos en cada interacción.

Conservamos el código del entregable anterior:

* Task
    * Estos campos ya estaban:
    * id 
    * title
    * description
    * priority
    * effort_hours
    * status
    * assigned_to
    * Nuevos campos
    * category --> Nuevo campo puede ser str o enum
    * risk_analysis --> Nuevo campo texto
    * risk_mitigation --> Nuevo campo texto

Endpoints CRUD (Estos ya estaban, no hace falta modificarlos)

* Crear POST /tasks
* Leer GET /tasks
* Leer una GET /tasks/{id}
* Actualizar PUT /tasks/{id}
* Eliminar DELETE /tasks/{id}

Agregamos 4 nuevos endpoints que usen LLMs:

* POST /ai/tasks/describe recibe una task con description vacía y genera su description con LLM a partir del resto de campos como el title. Este endpoint podría devolver la misma tarea que ha recibido pero con el campo description relleno.

* POST /ai/tasks/categorize recibe una tarea sin categoría y con LLM debe poder clasificarla bajo una categoría: Frontend, Backend, Testing, Infra, etc. Este endpoint podría devolver la misma tarea que ha recibido pero con el campo category relleno. El LLM debería devolver únicamente la categoría, por ejemplo:
    * Formulario de registro para usuarios administradores portal web Angular --> Frontend

* POST /ai/tasks/estimate: recibe una tarea sin effort_hours y con LLM debe poder estimar su esfuerzo en horas leyendo su title, description y category. Este endpoint podría devolver la misma tarea que ha recibido pero con el campo effort_hours relleno, importante, es un campo numérico no de texto, por lo que habrá que hacer parsing.
    * Entra titulo, description, category --> horas (número)
    * Al LLM le podemos pasar titulo, descripcion, category --> 8

* POST /ai/tasks/audit: recibe una tarea con todos los campos rellenos menos risk_analysis y risk_mitigation. Con esa tarea utiliza sus datos para lanzar dos peticiones un LLM. 
    * Una primera petición para obtener un análisis de riesgos que puedan surgir en la tarea y almacenarlo en risk_analysis
    * una segunda petición que use esa info junto a la de la tarea para pedir un plan de mitigación de riesgos que se almacene en risk_mitigation.

No es obligatorio que las salidas del LLM sean en JSON, serán texto normal.

Para cada petición a LLMs, será necesario un system prompt donde se especifique el rol y la salida deseada, y el user prompt que pase lo que sea específico para esa tarea en concreto.

Hemos puesto POST por simplificar la parte del id, pero se puede usar PUT, PATCH.

La información generada se puede añadir a la Task que se esté procesando y devolver en el API REST, opcionalmente se puede almacenar en una lista o archivo.

* Entrega: m3_entregable2_nombre_apellido.py