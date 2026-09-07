from datetime import datetime


class Task:
    """Represents a single task in the TaskFlow application."""

    VALID_PRIORITIES = ["low", "medium", "high"]

    def __init__(
        self,
        task_id: int,
        title: str,
        priority: str = "medium",
        due_date: str = "",
        completed: bool = False,
    ):
        title_clean = title.strip() if title else ""
        if not title_clean:
            raise ValueError("Task title cannot be empty.")

        priority_clean = priority.lower().strip() if priority else "medium"
        if priority_clean not in self.VALID_PRIORITIES:
            raise ValueError(
                f"Invalid priority '{priority}'. Must be one of: "
                f"{', '.join(self.VALID_PRIORITIES)}"
            )

        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Due date must be in YYYY-MM-DD format.")

        self.id = task_id
        self.title = title_clean
        self.priority = priority_clean
        self.due_date = due_date
        self.completed = completed

    def to_dict(self) -> dict:
        """Serializes the task instance into a JSON-compatible dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "due_date": self.due_date,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Factory method to instantiate a Task from a dictionary."""
        return cls(
            task_id=data["id"],
            title=data["title"],
            priority=data.get("priority", "medium"),
            due_date=data.get("due_date", ""),
            completed=data.get("completed", False),
        )
