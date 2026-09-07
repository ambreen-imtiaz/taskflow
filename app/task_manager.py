from typing import List, Optional
from app.models import Task
from app.storage import Storage


class TaskManager:
    """Core manager handling task CRUD operations and state."""

    def __init__(self, storage: Optional[Storage] = None):
        self.storage = storage or Storage()
        self.tasks: List[Task] = self.storage.load_tasks()
        self._next_id = max([t.id for t in self.tasks], default=0) + 1

    def add_task(
        self, title: str, priority: str = "medium", due_date: str = ""
    ) -> Task:
        """Creates and persists a new task."""
        task = Task(
            task_id=self._next_id,
            title=title,
            priority=priority,
            due_date=due_date,
        )
        self.tasks.append(task)
        self._next_id += 1
        self.storage.save_tasks(self.tasks)
        return task

    def list_tasks(self, show_completed: bool = True) -> List[Task]:
        """Returns tasks, optionally filtered by completion status."""
        if show_completed:
            return self.tasks
        return [t for t in self.tasks if not t.completed]

    def mark_completed(self, task_id: int) -> bool:
        """Marks a task as completed by its ID."""
        task = self.get_task(task_id)
        if task:
            task.completed = True
            self.storage.save_tasks(self.tasks)
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """Deletes a task by its ID."""
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self.storage.save_tasks(self.tasks)
            return True
        return False

    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieves a task instance by its ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
