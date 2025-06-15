#!/usr/bin/env python3
"""
Test de los esquemas de validación de tareas, incluyendo los campos de IA.

Este test verifica que los esquemas de Pydantic para tareas (TaskCreateSchema, TaskSchema, etc.)
funcionan correctamente, tanto con los campos originales como con los nuevos campos relacionados con IA.
Incluye pruebas de retrocompatibilidad, validación de enums y manejo de errores de validación.
No modifica datos, solo valida instanciación y muestra resultados por consola.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pydantic import ValidationError

def test_task_schemas():
    """Prueba todos los esquemas de validación"""
    try:
        from app.schemas.task_schema import (
            TaskCategory, TaskCreateSchema, TaskSchema,
            TaskDescribeSchema, TaskCategorizeSchema, 
            TaskEstimateSchema, TaskAuditSchema
        )
        print("✅ Todos los esquemas importados correctamente")

        # Prueba 1: Enum TaskCategory
        print(f"\n📋 Categorías disponibles ({len(TaskCategory)}):")
        for category in TaskCategory:
            print(f"  - {category.value}")

        # Prueba 2: TaskCreateSchema con campos originales (retrocompatibilidad)
        task_original_data = {
            "title": "Tarea de prueba",
            "description": "Descripción de prueba",
            "priority": "alta",
            "effort_hours": 5.0,
            "status": "pendiente",
            "assigned_to": "Juan"
        }
        task_original = TaskCreateSchema(**task_original_data)
        print("✅ TaskCreateSchema con campos originales (retrocompatibilidad)")

        # Prueba 3: TaskCreateSchema con campos IA
        task_ia_data = {
            **task_original_data,
            "category": "Desarrollo",
            "token_usage": 42
        }
        task_ia = TaskCreateSchema(**task_ia_data)
        print("✅ TaskCreateSchema con campos IA")

        # Prueba 4: Validación de errores
        try:
            TaskCreateSchema(title=123)  # Error: title debe ser str
        except ValidationError as e:
            print(f"✅ Error de validación capturado: {e.errors()[0]['msg']}")

    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == "__main__":
    test_task_schemas()
