import sys
from app.task_manager import TaskManager


def print_menu():
    print("\n--- TaskFlow CLI ---")
    print("1. List Tasks")
    print("2. Add Task")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")


def main():
    manager = TaskManager()

    while True:
        print_menu()
        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            tasks = manager.list_tasks()
            if not tasks:
                print("\nNo tasks found.")
            else:
                print("\nTasks:")
                for task in tasks:
                    status = "✓" if task.completed else " "
                    due = f" (Due: {task.due_date})" if task.due_date else ""
                    print(
                        f"[{status}] {task.id}. {task.title} "
                        f"[{task.priority.upper()}]{due}"
                    )

        elif choice == "2":
            title = input("Enter task title: ").strip()
            if not title:
                print("Error: Title cannot be empty.")
                continue
            priority = input("Enter priority (low/medium/high) [medium]: ").strip()
            if not priority:
                priority = "medium"
            due_date = input("Enter due date (YYYY-MM-DD) [optional]: ").strip()

            try:
                task = manager.add_task(title, priority, due_date)
                print(f"Task '{task.title}' added successfully with ID {task.id}.")
            except ValueError as err:
                print(f"Error: {err}")

        elif choice == "3":
            try:
                task_id = int(input("Enter task ID to complete: ").strip())
                if manager.mark_completed(task_id):
                    print(f"Task {task_id} marked as completed.")
                else:
                    print(f"Task {task_id} not found.")
            except ValueError:
                print("Error: Please enter a valid numerical ID.")

        elif choice == "4":
            try:
                task_id = int(input("Enter task ID to delete: ").strip())
                if manager.delete_task(task_id):
                    print(f"Task {task_id} deleted successfully.")
                else:
                    print(f"Task {task_id} not found.")
            except ValueError:
                print("Error: Please enter a valid numerical ID.")

        elif choice == "5":
            print("Exiting TaskFlow CLI. Goodbye!")
            sys.exit(0)

        else:
            print("Invalid choice. Please select between 1 and 5.")


if __name__ == "__main__":
    main()
