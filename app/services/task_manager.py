"""
Implementa la clase TaskManager, responsable de la lógica de negocio y la gestión de tareas,
incluyendo la persistencia en archivo JSON.
"""
import os
from app.models.task import Task
from app.repositories.json_task_repository import JsonTaskRepository
from app.repositories.i_task_repository import ITaskRepository

class TaskManager:
    """
    Servicio para la gestión de tareas, desacoplado de la persistencia.

    Métodos:
        get_all(): Devuelve todas las tareas.
        get_by_id(task_id): Devuelve una tarea por su ID.
        create(task): Crea una nueva tarea.
        update(task_id, updated_task): Actualiza una tarea existente.
        delete(task_id): Elimina una tarea por su ID.
    """
    def __init__(self, repository: ITaskRepository = None):
        """
        Inicializa el TaskManager con un repositorio de tareas.

        Args:
            repository (ITaskRepository, opcional): Repositorio de tareas a utilizar. Si no se proporciona, se usa JsonTaskRepository por defecto.
        """
        if repository is None:
            data_path = os.path.join(os.path.dirname(__file__), '../data/tasks.json')
            repository = JsonTaskRepository(os.path.abspath(data_path))
        self.repository = repository

    def get_all(self):
        """
        Devuelve todas las tareas almacenadas.

        Returns:
            list[Task]: Lista de tareas.
        """
        return self.repository.load_tasks()

    def get_by_id(self, task_id):
        """
        Devuelve una tarea por su ID.

        Args:
            task_id (int): Identificador de la tarea.
        Returns:
            Task or None: Tarea encontrada o None si no existe.
        """
        tasks = self.repository.load_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        return None

    def create(self, task):
        """
        Crea una nueva tarea y la almacena. Si el id es None, lo autogenera.

        Args:
            task (Task): Tarea a crear.
        Returns:
            Task: La tarea creada.
        """
        tasks = self.repository.load_tasks()
        if task.id is None:
            max_id = max((t.id for t in tasks), default=0)
            task.id = max_id + 1
        tasks.append(task)
        self.repository.save_tasks(tasks)
        return task

    def update(self, task_id, updated_task):
        """
        Actualiza una tarea existente.

        Args:
            task_id (int): ID de la tarea a actualizar.
            updated_task (Task): Nueva información de la tarea.
        Returns:
            Task or None: Tarea actualizada o None si no existe.
        """
        tasks = self.repository.load_tasks()
        for idx, task in enumerate(tasks):
            if task.id == task_id:
                tasks[idx] = updated_task
                self.repository.save_tasks(tasks)
                return updated_task
        return None

    def delete(self, task_id):
        """
        Elimina una tarea por su ID.

        Args:
            task_id (int): ID de la tarea a eliminar.
        Returns:
            bool: True si la tarea fue eliminada, False si no existía.
        """
        tasks = self.repository.load_tasks()
        new_tasks = [task for task in tasks if task.id != task_id]
        if len(new_tasks) == len(tasks):
            return False
        self.repository.save_tasks(new_tasks)
        return True
