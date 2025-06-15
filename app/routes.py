"""
Define las rutas y controladores principales de la API Flask para la gestión de tareas.
"""
from flask import Blueprint, request, jsonify
from app.services.task_manager import TaskManager
from app.schemas.task_schema import TaskSchema
from app.models.task import Task

bp = Blueprint('tasks', __name__)
task_manager = TaskManager()

@bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = task_manager.get_all()
    return jsonify([task.to_dict() for task in tasks]), 200

@bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = task_manager.get_by_id(task_id)
    if not task:
        return jsonify({'error': 'Tarea no encontrada'}), 404
    return jsonify(task.to_dict()), 200

@bp.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.get_json()
        from app.schemas.task_schema import TaskCreateSchema
        validated = TaskCreateSchema(**data)
        # El id se generará automáticamente en TaskManager
        task = Task.from_dict(validated.dict())
        task_manager.create(task)
        return jsonify(task.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        data = request.get_json()
        validated = TaskSchema(**data)
        updated_task = Task.from_dict(validated.dict())
        result = task_manager.update(task_id, updated_task)
        if not result:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        return jsonify(result.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    result = task_manager.delete(task_id)
    if not result:
        return jsonify({'error': 'Tarea no encontrada'}), 404
    return jsonify({'message': 'Tarea eliminada'}), 200

