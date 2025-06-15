"""
Contiene la clase Task, que representa el modelo de dominio de una tarea, 
así como los métodos para convertir entre objetos y diccionarios.
"""

class Task:
    """
    Representa una tarea del sistema.

    Atributos:
        id (int): Identificador único de la tarea.
        title (str): Título de la tarea.
        description (str): Descripción detallada de la tarea.
        priority (str): Prioridad de la tarea ('baja', 'media', 'alta', 'bloqueante').
        effort_hours (float): Horas estimadas de esfuerzo.
        status (str): Estado de la tarea ('pendiente', 'en progreso', 'en revisión', 'completada').
        assigned_to (str): Persona asignada a la tarea.
        category (str): Categoría de la tarea (Frontend, Backend, Testing, etc.).
        risk_analysis (str): Análisis de riesgos generado por IA.
        risk_mitigation (str): Plan de mitigación de riesgos generado por IA.
        token_usage (int): Uso de tokens en la tarea.
    """
    def __init__(self, id=None, title=None, description=None, priority=None, effort_hours=None, status=None, assigned_to=None, category=None, risk_analysis=None, risk_mitigation=None, token_usage=0):
        """
        Inicializa una nueva instancia de Task.

        Args:
            id (int): Identificador único de la tarea.
            title (str): Título de la tarea.
            description (str): Descripción detallada de la tarea.
            priority (str): Prioridad de la tarea.
            effort_hours (float): Horas estimadas de esfuerzo.
            status (str): Estado de la tarea.
            assigned_to (str): Persona asignada a la tarea.
            category (str): Categoría de la tarea (Frontend, Backend, Testing, etc.).
            risk_analysis (str): Análisis de riesgos generado por IA.
            risk_mitigation (str): Plan de mitigación de riesgos generado por IA.
            token_usage (int): Uso de tokens en la tarea.
        """
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.effort_hours = effort_hours
        self.status = status
        self.assigned_to = assigned_to
        self.category = category
        self.risk_analysis = risk_analysis
        self.risk_mitigation = risk_mitigation
        self.token_usage = token_usage if token_usage is not None else 0

    def to_dict(self):
        """
        Convierte la tarea a un diccionario.

        Returns:
            dict: Representación de la tarea como diccionario.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "effort_hours": self.effort_hours,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "category": self.category,
            "risk_analysis": self.risk_analysis,
            "risk_mitigation": self.risk_mitigation,
            "token_usage": self.token_usage
        }

    @classmethod
    def from_dict(cls, data):
        """
        Crea una instancia de Task a partir de un diccionario.
        Mantiene retrocompatibilidad con tareas que no tienen los nuevos campos de IA.

        Args:
            data (dict): Diccionario con los datos de la tarea.
        Returns:
            Task: Instancia de la clase Task.
        """
        return cls(
            id=data.get("id"),
            title=data.get("title"),
            description=data.get("description"),
            priority=data.get("priority"),
            effort_hours=data.get("effort_hours"),
            status=data.get("status"),
            assigned_to=data.get("assigned_to"),
            category=data.get("category"),
            risk_analysis=data.get("risk_analysis"),
            risk_mitigation=data.get("risk_mitigation"),
            token_usage=data.get("token_usage", 0)
        )

    def is_ai_enhanced(self):
        """
        Verifica si la tarea tiene al menos un campo de IA completado.
        Returns:
            bool: True si category, risk_analysis o risk_mitigation no son None.
        """
        return any([
            self.category,
            self.risk_analysis,
            self.risk_mitigation
        ])

    def has_risk_analysis(self):
        """
        Verifica si la tarea tiene análisis de riesgos y mitigación completos.
        Returns:
            bool: True si ambos campos están presentes.
        """
        return bool(self.risk_analysis and self.risk_mitigation)

    def get_ai_fields_summary(self):
        """
        Devuelve un resumen del estado de los campos IA.
        Returns:
            dict: Estado de cada campo IA y resumen general.
        """
        return {
            "category": bool(self.category),
            "risk_analysis": bool(self.risk_analysis),
            "risk_mitigation": bool(self.risk_mitigation),
            "ai_enhanced": self.is_ai_enhanced(),
            "risk_complete": self.has_risk_analysis()
        }

    def clone_for_ai_operation(self, exclude_fields=None):
        """
        Crea una copia de la tarea excluyendo campos específicos (útil para IA).
        Args:
            exclude_fields (list): Lista de campos a excluir (por ejemplo, ['description']).
        Returns:
            Task: Nueva instancia de Task sin los campos excluidos.
        """
        if exclude_fields is None:
            exclude_fields = []
        data = self.to_dict()
        for field in exclude_fields:
            if field in data:
                data[field] = None
        return Task.from_dict(data)
