import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

"""
Pruebas de integración para los endpoints de IA usando Flask test client.
"""
import json
import pytest
from app import create_app
from app.models.task import Task
from app.services.task_manager import TaskManager

def setup_module(module):
    # Prepara tareas de ejemplo en el sistema
    tm = TaskManager()
    tm.create(Task(title="Tarea IA 1", description="", priority="alta", effort_hours=1, status="pendiente", assigned_to="Carlos"))
    tm.create(Task(title="Tarea IA 2", description="", priority="media", effort_hours=2, status="pendiente", assigned_to="Maria"))

def teardown_module(module):
    # Limpia todas las tareas (opcional, según tu TaskManager)
    tm = TaskManager()
    tasks = tm.get_all()
    for t in tasks:
        tm.delete(t.id)

def test_ia_endpoints():
    app = create_app()
    client = app.test_client()
    # Obtén las tareas creadas
    tm = TaskManager()
    tasks = tm.get_all()
    for task in tasks:
        # 1. Descripción
        resp = client.post(f"/ai/tasks/describe/{task.id}")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "description" in data
        assert "token_usage" in data
        # 2. Categorizar
        resp = client.post(f"/ai/tasks/categorize/{task.id}")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "category" in data
        assert "token_usage" in data
        # 3. Estimar esfuerzo
        resp = client.post(f"/ai/tasks/estimate/{task.id}")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "effort_hours" in data
        assert "token_usage" in data
        # 4. Auditoría de riesgos
        resp = client.post(f"/ai/tasks/audit/{task.id}")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "risk_analysis" in data
        assert "risk_mitigation" in data
        assert "token_usage" in data
