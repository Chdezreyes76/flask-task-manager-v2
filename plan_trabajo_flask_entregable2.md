# 🧭 Plan de Trabajo — Proyecto Flask: Entregable 2 - Integración con IA (OpenAI SDK)

Este documento detalla el plan de desarrollo para extender la aplicación Flask del Entregable 1 con capacidades de Inteligencia Artificial utilizando el SDK de OpenAI. Se mantiene la arquitectura desacoplada y escalable del entregable anterior, añadiendo nuevos campos al modelo Task y 4 nuevos endpoints especializados en IA.

---

## 📋 RESUMEN DE CAMBIOS REQUERIDOS

### ✨ Nuevos campos en el modelo Task:
- `category` → Nuevo campo (str o enum): Frontend, Backend, Testing, Infra, etc.
- `risk_analysis` → Nuevo campo texto para análisis de riesgos
- `risk_mitigation` → Nuevo campo texto para plan de mitigación de riesgos

### 🤖 Nuevos endpoints con IA:
- `POST /ai/tasks/describe` → Generar descripción con LLM
- `POST /ai/tasks/categorize` → Clasificar tarea por categoría con LLM
- `POST /ai/tasks/estimate` → Estimar esfuerzo en horas con LLM
- `POST /ai/tasks/audit` → Análisis de riesgos y mitigación con LLM

### 📊 Monitoreo de tokens:
- Registrar el número de tokens consumidos en cada interacción con OpenAI

---

## 🧩 FASE 0: Preparación del entorno para IA

### 🎯 Objetivo
Configurar el entorno para trabajar con APIs de IA y gestionar tokens de consumo.

### ✅ Tareas

- **Instalar nuevas dependencias:**
  ```bash
  pip install openai tiktoken python-dotenv
  ```
- **Actualizar `requirements.txt`** con las nuevas dependencias:
  ```
  openai>=1.0.0
  tiktoken>=0.5.0
  python-dotenv>=1.0.0
  ```
- **Configurar variables de entorno** para la API key de OpenAI:
  - Crear archivo `.env` en la raíz del proyecto
  - Añadir `OPENAI_API_KEY=tu_api_key_aqui`
  - Actualizar `.gitignore` para excluir `.env`
- **Crear servicio de configuración** en `app/config/ai_config.py`:
  - Cargar variables de entorno
  - Configurar cliente OpenAI
  - Definir modelos y parámetros por defecto

---

## 🧱 FASE 1: Extensión del modelo Task y esquemas

### 🎯 Objetivo
Añadir los nuevos campos al modelo de dominio y actualizarlo en todos los niveles de la arquitectura.

### ✅ Tareas

- **Actualizar `app/models/task.py`:**
  - Añadir campos: `category`, `risk_analysis`, `risk_mitigation`
  - Modificar `__init__`, `to_dict()` y `from_dict()`
  - Mantener retrocompatibilidad con tareas existentes

- **Actualizar `app/schemas/task_schema.py`:**
  - Crear enum `TaskCategory` para categorías válidas
  - Añadir validaciones para los nuevos campos
  - Crear esquemas específicos para cada endpoint de IA:
    - `TaskDescribeSchema` (sin description)
    - `TaskCategorizeSchema` (sin category)
    - `TaskEstimateSchema` (sin effort_hours)
    - `TaskAuditSchema` (sin risk_analysis y risk_mitigation)

- **Verificar compatibilidad:**
  - Ejecutar pruebas existentes para asegurar que no hay regresiones
  - Actualizar archivo `tasks.json` de prueba si es necesario

---

## 🤖 FASE 2: Servicio de IA para interacción con OpenAI

### 🎯 Objetivo
Crear un servicio centralizado para manejar todas las interacciones con OpenAI, incluyendo el monitoreo de tokens (sin persistencia separada).

### ✅ Tareas

- **Crear `app/services/ai_service.py`:**
  - Clase `OpenAIService` con métodos para cada tipo de petición
  - Sistema de prompts (system + user) parametrizables
  - Manejo de errores de API (rate limits, errores de red, etc.)
  - Contador de tokens usando tiktoken

- **Métodos específicos en `OpenAIService`:**
  - `generate_description(task_data)` → Para endpoint describe
  - `categorize_task(task_data)` → Para endpoint categorize
  - `estimate_effort(task_data)` → Para endpoint estimate
  - `analyze_risks(task_data)` → Para endpoint audit (análisis)
  - `generate_mitigation(task_data, risk_analysis)` → Para endpoint audit (mitigación)

---

## 🧮 FASE 2B: Acumulación de tokens en la tarea

### 🎯 Objetivo
Registrar y acumular el número de tokens consumidos por cada tarea directamente en el modelo y esquema de la Task.

### ✅ Tareas

- **Modificar `app/models/task.py`:**
  - Añadir campo `token_usage` (int, por defecto 0) para almacenar el total acumulado de tokens consumidos por la tarea.
  - Actualizar métodos `__init__`, `to_dict()` y `from_dict()` para soportar el nuevo campo.
- **Modificar `app/schemas/task_schema.py`:**
  - Añadir campo `token_usage` en los esquemas de tarea.
  - Validar que sea un entero >= 0.
- **Integrar la lógica de acumulación de tokens en las fases 3 y 4 (ver detalles en cada fase).**
- (Opcional) Mostrar el coste estimado acumulado junto con el campo de tokens.

---

## 🛠️ FASE 3: Manager de IA para lógica de negocio (mejorada)

### 🎯 Objetivo
Crear un manager que orqueste las operaciones de IA manteniendo la separación de responsabilidades y actualice el campo de tokens acumulados.

### ✅ Tareas

- **Crear `app/services/ai_task_manager.py`:**
  - Clase `AITaskManager` que utiliza `OpenAIService` y `TaskManager`
  - Métodos que implementan la lógica de cada endpoint de IA
  - Validación de datos antes de enviar a OpenAI
  - Post-procesamiento de respuestas (parsing, limpieza, validación)
  - **En cada método, sumar los tokens consumidos (devueltos por OpenAIService) al campo `token_usage` de la tarea y persistir el valor actualizado.**

- **Métodos principales:**
  - `describe_task(task)` → Genera description y actualiza la tarea
  - `categorize_task(task)` → Clasifica y asigna category
  - `estimate_task_effort(task)` → Estima effort_hours (parsing a número)
  - `audit_task_risks(task)` → Genera risk_analysis y risk_mitigation

- **Integración con TaskManager:**
  - Reutilizar TaskManager existente para persistencia
  - Mantener separación entre lógica de IA y lógica de dominio

---

## 🌐 FASE 4: Nuevas rutas para endpoints de IA (mejorada)

### 🎯 Objetivo
Implementar los 4 nuevos endpoints RESTful que integren las capacidades de IA y aseguren la actualización del campo `token_usage` en cada operación.

### ✅ Tareas

- **Crear `app/routes/ai_routes.py`:**
  - Nuevo Blueprint para rutas de IA: `ai_tasks`
  - Separar responsabilidades: rutas de CRUD vs rutas de IA

- **Implementar endpoints específicos:**

  1. **`POST /ai/tasks/describe`:**
     - Recibe: Task con description vacía
     - Valida: Todos los campos excepto description
     - Llama al manager de IA, actualiza y persiste el campo `token_usage` de la tarea
     - Retorna: Task con description generada y tokens acumulados

  2. **`POST /ai/tasks/categorize`:**
     - Recibe: Task sin category
     - Valida: Todos los campos excepto category  
     - Llama al manager de IA, actualiza y persiste el campo `token_usage` de la tarea
     - Retorna: Task con category asignada y tokens acumulados

  3. **`POST /ai/tasks/estimate`:**
     - Recibe: Task sin effort_hours
     - Valida: title, description, category obligatorios
     - Llama al manager de IA, actualiza y persiste el campo `token_usage` de la tarea
     - Retorna: Task con effort_hours estimado (número) y tokens acumulados

  4. **`POST /ai/tasks/audit`:**
     - Recibe: Task completa excepto risk_analysis y risk_mitigation
     - Genera: Análisis de riesgos y plan de mitigación
     - Llama al manager de IA, actualiza y persiste el campo `token_usage` de la tarea
     - Retorna: Task con ambos campos completados y tokens acumulados

- **Manejo de errores específicos de IA:**
  - Rate limits de OpenAI
  - Errores de parsing (ej: effort_hours no numérico)
  - Timeouts de API
  - Respuestas vacías o inválidas

- **Registrar el nuevo Blueprint** en `app/__init__.py`

---

## 📊 FASE 5: Monitoreo y logging de tokens

### 🎯 Objetivo
Implementar un sistema de monitoreo del consumo de tokens y costos de OpenAI.

### ✅ Tareas

- **Crear `app/services/token_monitor.py`:**
  - Decorador para medir automáticamente el consumo de tokens
  - Cálculo de costos estimados por modelo
  - Logs detallados de cada operación

- **Crear endpoints de monitoreo:**
  - `GET /ai/stats/tokens` → Estadísticas de consumo total
  - `GET /ai/stats/operations` → Consumo por tipo de operación
  - `GET /ai/stats/costs` → Estimación de costos

- **Dashboard básico en endpoint:**
  - Resumen de tokens consumidos hoy/semana/mes
  - Operación más costosa
  - Promedio de tokens por operación

---

## 🧪 FASE 6: Pruebas automatizadas para IA

### 🎯 Objetivo
Extender las pruebas existentes para cubrir las nuevas funcionalidades de IA.

### ✅ Tareas

- **Crear `tests/test_ai_endpoints.py`:**
  - Pruebas para cada endpoint de IA
  - Mocks de OpenAI para evitar consumo real de tokens
  - Pruebas de manejo de errores específicos de IA

- **Crear `tests/test_ai_services.py`:**
  - Pruebas unitarias para `OpenAIService`
  - Pruebas de parsing y validación de respuestas
  - Pruebas de contador de tokens

- **Actualizar `tests/test_tasks.py`:**
  - Verificar compatibilidad con nuevos campos
  - Pruebas de migración de datos existentes

- **Crear fixtures para IA:**
  - Respuestas mockeadas de OpenAI
  - Tareas de ejemplo para cada tipo de operación
  - Configuración de testing sin consumir API real

---

## 📚 FASE 7: Actualización de documentación

### 🎯 Objetivo
Documentar las nuevas funcionalidades y actualizar la guía de uso.

### ✅ Tareas

- **Actualizar `README.md`:**
  - Sección de configuración de OpenAI API
  - Documentación de nuevos endpoints
  - Ejemplos de uso de cada endpoint de IA
  - Información sobre monitoreo de tokens

- **Actualizar `proyecto_tareas.ipynb`:**
  - Ejemplos prácticos de cada endpoint de IA
  - Cómo interpretar las respuestas de IA
  - Monitoreo de consumo de tokens
  - Casos de uso reales

- **Docstrings actualizados:**
  - Documentar todos los nuevos métodos y clases
  - Incluir información sobre tokens y costos
  - Ejemplos de uso en docstrings principales

---

## ⚡ FASE 8: Optimización y mejores prácticas

### 🎯 Objetivo
Optimizar el rendimiento y implementar mejores prácticas para producción.

### ✅ Tareas

- **Optimización de prompts:**
  - Refinar prompts para mayor precisión
  - Minimizar tokens sin perder calidad
  - Implementar prompt templates reutilizables

- **Caché de respuestas:**
  - Caché simple para evitar repetir consultas idénticas
  - TTL configurable para respuestas de IA

- **Rate limiting:**
  - Implementar límites por usuario/IP
  - Manejo graceful de rate limits de OpenAI

- **Configuración por entornos:**
  - Configuración específica para dev/test/prod
  - Modelos diferentes según entorno
  - Límites de tokens por entorno

---

## 📦 FASE FINAL: Empaquetado y entrega

### ✅ Tareas

- **Verificación final:**
  - Todas las pruebas pasan (incluyendo las nuevas)
  - Todos los endpoints funcionan correctamente
  - Documentación actualizada y completa
  - Variables de entorno documentadas

- **Limpieza de código:**
  - Eliminar código comentado
  - Revisar imports no utilizados
  - Verificar estilo de código consistente

- **Empaquetado:**
  - Crear `m3_entregable2_nombre_apellido.zip`
  - Incluir `.env.example` con estructura de variables
  - Excluir `.env` real (con API keys)
  - Incluir archivo de migración de datos si es necesario

---

## ✅ CHECKLIST DE VERIFICACIÓN FINAL

### 🎯 Verificación exhaustiva antes de la entrega

- [ ] **Configuración:**
  - [ ] OpenAI API key configurada correctamente
  - [ ] Todas las dependencias instaladas (`pip install -r requirements.txt`)
  - [ ] Variables de entorno documentadas en `.env.example`

- [ ] **Modelo extendido:**
  - [ ] Clase `Task` incluye nuevos campos: `category`, `risk_analysis`, `risk_mitigation`
  - [ ] Esquemas de validación actualizados
  - [ ] Retrocompatibilidad con datos existentes mantenida

- [ ] **Endpoints de IA implementados:**
  - [ ] `POST /ai/tasks/describe` funciona correctamente
  - [ ] `POST /ai/tasks/categorize` clasifica apropiadamente
  - [ ] `POST /ai/tasks/estimate` retorna número válido de horas
  - [ ] `POST /ai/tasks/audit` genera análisis y mitigación

- [ ] **Servicios de IA:**
  - [ ] `OpenAIService` maneja todas las interacciones con OpenAI
  - [ ] Contador de tokens funciona correctamente
  - [ ] Manejo de errores robusto (rate limits, timeouts, etc.)

- [ ] **Monitoreo:**
  - [ ] Tokens consumidos se registran correctamente
  - [ ] Endpoints de estadísticas funcionan
  - [ ] Logs detallados de operaciones de IA

- [ ] **Pruebas:**
  - [ ] Todas las pruebas existentes siguen pasando
  - [ ] Nuevas pruebas para endpoints de IA implementadas
  - [ ] Pruebas usan mocks (no consumen API real)

- [ ] **Documentación:**
  - [ ] `README.md` actualizado con nueva funcionalidad
  - [ ] `proyecto_tareas.ipynb` incluye ejemplos de IA
  - [ ] Docstrings añadidos a todas las nuevas clases y métodos

- [ ] **Funcionalidad manual verificada:**
  - [ ] Servidor Flask arranca sin errores
  - [ ] Endpoints CRUD originales siguen funcionando
  - [ ] Cada endpoint de IA retorna respuestas válidas
  - [ ] Monitoreo de tokens muestra datos correctos

---

## 🎯 ENTREGABLE

**Archivo:** `m3_entregable2_nombre_apellido.zip`

**Contenido mínimo:**
- Código fuente completo con extensiones de IA
- `requirements.txt` actualizado
- `.env.example` con estructura de variables
- `README.md` con documentación completa
- `proyecto_tareas.ipynb` con ejemplos
- Archivos de prueba actualizados
- Datos de ejemplo en `tasks.json`

**Exclusiones:**
- Carpeta `venv/`
- Archivo `.env` (con API keys reales)
- Carpetas `__pycache__/`
- Archivos temporales del sistema

---

✅ **¡Proyecto listo para entregar cuando todos los puntos estén verificados!**
