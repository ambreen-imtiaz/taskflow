import pytest
from app.models import Task


def test_task_creation_success():
    """Verify standard Task object creation with valid inputs."""
    task = Task(
        task_id=1,
        title="Prepare Exam Demo",
        priority="high",
        due_date="2026-10-15",
    )
    assert task.id == 1
    assert task.title == "Prepare Exam Demo"
    assert task.priority == "high"
    assert task.due_date == "2026-10-15"
    assert task.completed is False


def test_task_creation_empty_title_raises_error():
    """Verify that creating a task with empty title raises ValueError."""
    with pytest.raises(ValueError, match="Task title cannot be empty."):
        Task(task_id=1, title="   ")


def test_task_creation_invalid_priority_raises_error():
    """Verify that an unsupported priority level raises ValueError."""
    with pytest.raises(ValueError, match="Invalid priority 'urgent'"):
        Task(task_id=1, title="Valid Title", priority="urgent")


def test_task_creation_invalid_date_format_raises_error():
    """Verify that invalid date formats raise ValueError."""
    with pytest.raises(
        ValueError, match="Due date must be in YYYY-MM-DD format."
    ):
        Task(task_id=1, title="Valid Title", due_date="15-10-2026")


def test_task_to_dict_and_from_dict():
    """Verify serialization and deserialization accuracy."""
    original_task = Task(
        task_id=2,
        title="Test Serialization",
        priority="low",
        due_date="2026-12-01",
        completed=True,
    )
    data = original_task.to_dict()
    reconstructed_task = Task.from_dict(data)

    assert reconstructed_task.id == original_task.id
    assert reconstructed_task.title == original_task.title
    assert reconstructed_task.priority == original_task.priority
    assert reconstructed_task.due_date == original_task.due_date
    assert reconstructed_task.completed == original_task.completed
