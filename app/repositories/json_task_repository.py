"""
Repositorio para la persistencia de tareas en un archivo JSON.
"""
import json
import os
from app.models.task import Task
from app.repositories.i_task_repository import ITaskRepository

class JsonTaskRepository(ITaskRepository):
    """
    Repositorio para la persistencia de tareas en un archivo JSON.

    Métodos:
        load_tasks(): Carga todas las tareas desde el archivo JSON.
        save_tasks(tasks): Guarda la lista de tareas en el archivo JSON.
    """
    def __init__(self, filepath):
        """
        Inicializa el repositorio con la ruta al archivo JSON.

        Args:
            filepath (str): Ruta al archivo JSON donde se almacenan las tareas.
        """
        self.filepath = filepath
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def load_tasks(self):
        """
        Carga todas las tareas desde el archivo JSON.

        Returns:
            list[Task]: Lista de instancias de Task.
        """
        if os.path.getsize(self.filepath) == 0:
            return []
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return [Task.from_dict(item) for item in data]

    def save_tasks(self, tasks):
        """
        Guarda la lista de tareas en el archivo JSON.

        Args:
            tasks (list[Task]): Lista de tareas a guardar.
        """
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([task.to_dict() for task in tasks], f, ensure_ascii=False, indent=2)
