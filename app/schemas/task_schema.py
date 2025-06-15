"""
Define el esquema de validación TaskSchema usando Pydantic para validar los datos de las tareas.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional
from enum import Enum


class TaskCategory(str, Enum):
    FRONTEND = "Frontend"
    BACKEND = "Backend"
    TESTING = "Testing"
    DEVOPS = "DevOps"
    DATABASE = "Database"
    DOCUMENTATION = "Documentation"
    SECURITY = "Security"
    PERFORMANCE = "Performance"
    BUG_FIX = "Bug Fix"
    FEATURE = "Feature"


class TaskCreateSchema(BaseModel):
    """
    Esquema de validación para la creación de una tarea (sin id).

    Valida los atributos de una tarea y asegura que cumplen con los requisitos de tipo y formato.
    """

    title: str = Field(..., min_length=1, max_length=100, description="Título de la tarea")
    description: str = Field(..., min_length=1, description="Descripción de la tarea")
    priority: Literal['baja', 'media', 'alta', 'bloqueante'] = Field(..., description="Prioridad de la tarea")
    effort_hours: float = Field(..., gt=0, description="Horas estimadas de esfuerzo")
    status: Literal['pendiente', 'en progreso', 'en revisión', 'completada'] = Field(..., description="Estado de la tarea")
    assigned_to: str = Field(..., min_length=1, description="Persona asignada a la tarea")
    category: Optional[TaskCategory] = Field(None, description="Categoría de la tarea clasificada por IA")
    risk_analysis: Optional[str] = Field(None, min_length=1, description="Análisis de riesgos generado por IA")
    risk_mitigation: Optional[str] = Field(None, min_length=1, description="Plan de mitigación de riesgos generado por IA")
    token_usage: int = Field(0, ge=0, description="Tokens acumulados consumidos por la tarea")

    @field_validator('title', 'description', 'assigned_to', 'risk_analysis', 'risk_mitigation')
    @classmethod
    def not_empty(cls, v):
        """
        Valida que los campos de texto no estén vacíos.

        Args:
            v (str): Valor del campo.
        Returns:
            str: Valor validado.
        Raises:
            ValueError: Si el campo está vacío.
        """
        if v is not None and (not v or not v.strip()):
            raise ValueError('El campo no puede estar vacío')
        return v


class TaskSchema(TaskCreateSchema):
    """
    Esquema de validación para una tarea completa (incluye id).
    """

    id: int = Field(..., description="Identificador único de la tarea")


# =============================
# Esquemas específicos para IA
# =============================

class TaskDescribeSchema(BaseModel):
    """
    Esquema para POST /ai/tasks/describe (sin description)
    """
    title: str = Field(..., min_length=1, max_length=100)
    priority: Literal['baja', 'media', 'alta', 'bloqueante']
    effort_hours: Optional[float] = Field(None, gt=0)
    status: Literal['pendiente', 'en progreso', 'en revisión', 'completada'] = 'pendiente'
    assigned_to: str = Field(..., min_length=1)
    category: Optional[TaskCategory] = None

    @field_validator('title', 'assigned_to')
    @classmethod
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El campo no puede estar vacío')
        return v

class TaskCategorizeSchema(BaseModel):
    """
    Esquema para POST /ai/tasks/categorize (sin category)
    """
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    priority: Literal['baja', 'media', 'alta', 'bloqueante']
    effort_hours: Optional[float] = Field(None, gt=0)
    status: Literal['pendiente', 'en progreso', 'en revisión', 'completada'] = 'pendiente'
    assigned_to: str = Field(..., min_length=1)

    @field_validator('title', 'description', 'assigned_to')
    @classmethod
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El campo no puede estar vacío')
        return v

class TaskEstimateSchema(BaseModel):
    """
    Esquema para POST /ai/tasks/estimate (sin effort_hours)
    """
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    category: TaskCategory
    priority: Literal['baja', 'media', 'alta', 'bloqueante'] = 'media'
    status: Literal['pendiente', 'en progreso', 'en revisión', 'completada'] = 'pendiente'
    assigned_to: str = Field(..., min_length=1)

    @field_validator('title', 'description', 'assigned_to')
    @classmethod
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El campo no puede estar vacío')
        return v

class TaskAuditSchema(BaseModel):
    """
    Esquema para POST /ai/tasks/audit (sin risk_analysis y risk_mitigation)
    """
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    priority: Literal['baja', 'media', 'alta', 'bloqueante']
    effort_hours: float = Field(..., gt=0)
    status: Literal['pendiente', 'en progreso', 'en revisión', 'completada']
    assigned_to: str = Field(..., min_length=1)
    category: Optional[TaskCategory] = None

    @field_validator('title', 'description', 'assigned_to')
    @classmethod
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El campo no puede estar vacío')
        return v
