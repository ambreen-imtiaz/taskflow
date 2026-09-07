from app.storage import Storage
from app.task_manager import TaskManager


def test_task_manager_crud_operations(tmp_path):
    """Verify complete CRUD flow in TaskManager using isolated temp storage."""
    file_path = tmp_path / "tasks.json"
    storage = Storage(filepath=str(file_path))
    manager = TaskManager(storage=storage)

    # 1. Add Task
    task1 = manager.add_task(
        title="Write Documentation", priority="high", due_date="2026-09-30"
    )
    assert task1.id == 1
    assert len(manager.list_tasks()) == 1

    # 2. Add Second Task
    task2 = manager.add_task(title="Record Video", priority="medium")
    assert task2.id == 2
    assert len(manager.list_tasks()) == 2

    # 3. Mark Completed
    assert manager.mark_completed(1) is True
    assert manager.get_task(1).completed is True
    assert len(manager.list_tasks(show_completed=False)) == 1

    # 4. Delete Task
    assert manager.delete_task(2) is True
    assert len(manager.list_tasks()) == 1
    assert manager.get_task(2) is None


def test_mark_completed_non_existent_id(tmp_path):
    """Verify marking invalid ID completed returns False safely."""
    storage = Storage(filepath=str(tmp_path / "tasks.json"))
    manager = TaskManager(storage=storage)
    assert manager.mark_completed(99) is False
