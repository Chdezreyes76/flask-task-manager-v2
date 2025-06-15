"""
AITaskManager: Orquesta operaciones de IA y actualiza el campo token_usage en cada tarea.
"""
from app.services.ai_service import OpenAIService
from app.services.task_manager import TaskManager
from app.models.task import Task

class AITaskManager:
    def __init__(self, task_manager=None, ai_service=None):
        self.task_manager = task_manager or TaskManager()
        self.ai_service = ai_service or OpenAIService()

    def describe_task(self, task_id):
        """
        Genera una descripción para la tarea indicada usando IA, actualiza el campo description,
        acumula los tokens consumidos en token_usage y persiste la tarea actualizada.
        Args:
            task_id (int): ID de la tarea a procesar.
        Returns:
            (Task, str): La tarea actualizada y un mensaje de error (None si no hay error).
        """
        task = self.task_manager.get_by_id(task_id)
        if not task:
            return None, 'Tarea no encontrada'
        result = self.ai_service.generate_description(task.to_dict())
        if 'error' in result:
            return None, result['error']
        task.description = result['result']
        tokens = result.get('total_tokens', 0) or 0
        task.token_usage = (task.token_usage or 0) + tokens
        self.task_manager.update(task_id, task)
        return task, None

    def categorize_task(self, task_id):
        """
        Clasifica la tarea indicada usando IA, actualiza el campo category,
        acumula los tokens consumidos en token_usage y persiste la tarea actualizada.
        Args:
            task_id (int): ID de la tarea a procesar.
        Returns:
            (Task, str): La tarea actualizada y un mensaje de error (None si no hay error).
        """
        task = self.task_manager.get_by_id(task_id)
        if not task:
            return None, 'Tarea no encontrada'
        result = self.ai_service.categorize_task(task.to_dict())
        if 'error' in result:
            return None, result['error']
        task.category = result['result']
        tokens = result.get('total_tokens', 0) or 0
        task.token_usage = (task.token_usage or 0) + tokens
        self.task_manager.update(task_id, task)
        return task, None

    def estimate_task_effort(self, task_id):
        """
        Estima el esfuerzo en horas para la tarea indicada usando IA, actualiza el campo effort_hours,
        acumula los tokens consumidos en token_usage y persiste la tarea actualizada.
        Args:
            task_id (int): ID de la tarea a procesar.
        Returns:
            (Task, str): La tarea actualizada y un mensaje de error (None si no hay error).
        """
        task = self.task_manager.get_by_id(task_id)
        if not task:
            return None, 'Tarea no encontrada'
        result = self.ai_service.estimate_effort(task.to_dict())
        if 'error' in result:
            return None, result['error']
        try:
            task.effort_hours = float(result['result'])
        except Exception:
            return None, 'No se pudo parsear el esfuerzo estimado'
        tokens = result.get('total_tokens', 0) or 0
        task.token_usage = (task.token_usage or 0) + tokens
        self.task_manager.update(task_id, task)
        return task, None

    def audit_task_risks(self, task_id):
        """
        Genera el análisis de riesgos y el plan de mitigación para la tarea indicada usando IA,
        actualiza los campos risk_analysis y risk_mitigation, acumula los tokens consumidos en token_usage
        y persiste la tarea actualizada.
        Args:
            task_id (int): ID de la tarea a procesar.
        Returns:
            (Task, str): La tarea actualizada y un mensaje de error (None si no hay error).
        """
        task = self.task_manager.get_by_id(task_id)
        if not task:
            return None, 'Tarea no encontrada'
        # 1. Análisis de riesgos
        result_risk = self.ai_service.analyze_risks(task.to_dict())
        if 'error' in result_risk:
            return None, result_risk['error']
        task.risk_analysis = result_risk['result']
        tokens_risk = result_risk.get('total_tokens', 0) or 0
        # 2. Plan de mitigación
        result_mitigation = self.ai_service.generate_mitigation(task.to_dict(), task.risk_analysis)
        if 'error' in result_mitigation:
            return None, result_mitigation['error']
        task.risk_mitigation = result_mitigation['result']
        tokens_mitigation = result_mitigation.get('total_tokens', 0) or 0
        # Acumular ambos consumos
        task.token_usage = (task.token_usage or 0) + tokens_risk + tokens_mitigation
        self.task_manager.update(task_id, task)
        return task, None
