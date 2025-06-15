"""
Interfaz para los repositorios de tareas. Permite desacoplar la lógica de negocio de la persistencia.
"""
from abc import ABC, abstractmethod
from typing import List
from app.models.task import Task

class ITaskRepository(ABC):
    """
    Interfaz abstracta para repositorios de tareas.

    Define los métodos que cualquier repositorio de tareas debe implementar.
    """
    @abstractmethod
    def load_tasks(self) -> List[Task]:
        """
        Carga todas las tareas desde la fuente de datos.

        Returns:
            list[Task]: Lista de instancias de Task.
        """
        pass

    @abstractmethod
    def save_tasks(self, tasks: List[Task]):
        """
        Guarda la lista de tareas en la fuente de datos.

        Args:
            tasks (list[Task]): Lista de tareas a guardar.
        """
        pass
