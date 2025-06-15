"""
Rutas para los endpoints de IA que utilizan AITaskManager y devuelven el campo token_usage actualizado.
"""
from flask import Blueprint, request, jsonify
from app.services.ai_task_manager import AITaskManager

ai_bp = Blueprint('ai_tasks', __name__)
ai_manager = AITaskManager()

@ai_bp.route('/ai/tasks/describe/<int:task_id>', methods=['POST'])
def describe_task(task_id):
    task, error = ai_manager.describe_task(task_id)
    if error:
        return jsonify({'error': error}), 400
    return jsonify(task.to_dict()), 200

@ai_bp.route('/ai/tasks/categorize/<int:task_id>', methods=['POST'])
def categorize_task(task_id):
    task, error = ai_manager.categorize_task(task_id)
    if error:
        return jsonify({'error': error}), 400
    return jsonify(task.to_dict()), 200

@ai_bp.route('/ai/tasks/estimate/<int:task_id>', methods=['POST'])
def estimate_task_effort(task_id):
    task, error = ai_manager.estimate_task_effort(task_id)
    if error:
        return jsonify({'error': error}), 400
    return jsonify(task.to_dict()), 200

@ai_bp.route('/ai/tasks/audit/<int:task_id>', methods=['POST'])
def audit_task_risks(task_id):
    task, error = ai_manager.audit_task_risks(task_id)
    if error:
        return jsonify({'error': error}), 400
    return jsonify(task.to_dict()), 200
