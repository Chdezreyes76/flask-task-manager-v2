"""
Incluye las pruebas unitarias para las funcionalidades principales de la gestión de tareas.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app.models.task import Task
from app.services.task_manager import TaskManager
from app.repositories.json_task_repository import JsonTaskRepository
import tempfile
import json


@pytest.fixture
def temp_json_repo():
    # Crear un archivo temporal para pruebas
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    # Inicializar el archivo con una lista vacía para evitar errores de JSONDecodeError
    with open(path, 'w', encoding='utf-8') as f:
        f.write('[]')
    repo = JsonTaskRepository(path)
    yield repo
    os.remove(path)

@pytest.fixture
def task_manager(temp_json_repo):
    return TaskManager(repository=temp_json_repo)

@pytest.fixture
def sample_task():
    return Task(
        id=1,
        title="Tarea de prueba",
        description="Descripción de prueba",
        priority="media",
        effort_hours=2.5,
        status="pendiente",
        assigned_to="Carlos"
    )

def test_create_and_get_task(task_manager, sample_task):
    print("[TEST] Creando y obteniendo tarea...")
    task_manager.create(sample_task)
    tasks = task_manager.get_all()
    assert len(tasks) == 1
    assert tasks[0].title == "Tarea de prueba"
    task = task_manager.get_by_id(1)
    assert task is not None
    assert task.id == 1
    print("[OK] test_create_and_get_task completado")

def test_update_task(task_manager, sample_task):
    print("[TEST] Actualizando tarea...")
    task_manager.create(sample_task)
    updated = Task(
        id=1,
        title="Tarea actualizada",
        description="Nueva descripción",
        priority="alta",
        effort_hours=3.0,
        status="en progreso",
        assigned_to="Ana"
    )
    result = task_manager.update(1, updated)
    assert result is not None
    assert result.title == "Tarea actualizada"
    task = task_manager.get_by_id(1)
    assert task.title == "Tarea actualizada"
    print("[OK] test_update_task completado")

def test_delete_task(task_manager, sample_task):
    print("[TEST] Eliminando tarea...")
    task_manager.create(sample_task)
    deleted = task_manager.delete(1)
    assert deleted is True
    assert task_manager.get_by_id(1) is None
    print("[OK] test_delete_task completado")

def test_delete_nonexistent_task(task_manager):
    print("[TEST] Eliminando tarea inexistente...")
    deleted = task_manager.delete(999)
    assert deleted is False
    print("[OK] test_delete_nonexistent_task completado")

def test_get_nonexistent_task(task_manager):
    print("[TEST] Buscando tarea inexistente...")
    assert task_manager.get_by_id(999) is None
    print("[OK] test_get_nonexistent_task completado")

