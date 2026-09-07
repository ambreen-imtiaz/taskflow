import json
import os
from typing import List
from app.models import Task


class Storage:
    """Handles JSON file persistence for tasks."""

    def __init__(self, filepath: str = "tasks.json"):
        self.filepath = filepath

    def save_tasks(self, tasks: List[Task]) -> None:
        """Saves a list of Task objects to a JSON file."""
        data = [task.to_dict() for task in tasks]
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load_tasks(self) -> List[Task]:
        """Loads tasks from a JSON file. Returns empty list if missing/corrupt."""
        if not os.path.exists(self.filepath):
            return []

        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                if not isinstance(data, list):
                    return []
                return [Task.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError, ValueError):
            return []
