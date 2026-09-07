from app.models import Task
from app.storage import Storage


def test_save_and_load_tasks(tmp_path):
    """Verify saving tasks to JSON and reloading them maintains integrity."""
    file_path = tmp_path / "test_tasks.json"
    storage = Storage(filepath=str(file_path))

    tasks = [
        Task(task_id=1, title="Task 1", priority="high"),
        Task(task_id=2, title="Task 2", priority="low", completed=True),
    ]

    storage.save_tasks(tasks)
    loaded_tasks = storage.load_tasks()

    assert len(loaded_tasks) == 2
    assert loaded_tasks[0].title == "Task 1"
    assert loaded_tasks[1].completed is True


def test_load_non_existent_file(tmp_path):
    """Verify loading from missing file safely returns an empty list."""
    file_path = tmp_path / "missing.json"
    storage = Storage(filepath=str(file_path))
    assert storage.load_tasks() == []


def test_load_corrupted_json(tmp_path):
    """Verify corrupt JSON gracefully degrades to empty list without crash."""
    file_path = tmp_path / "corrupt.json"
    file_path.write_text("invalid json contents")

    storage = Storage(filepath=str(file_path))
    assert storage.load_tasks() == []
