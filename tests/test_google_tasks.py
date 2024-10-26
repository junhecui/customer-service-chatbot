from src.integrations.google_tasks import add_task, list_tasks
import datetime

def test_add_task():
    print("\nTest 1: Adding a task with only a title")
    add_task("Test Task 1 - Title Only")
    print("Task with title only added successfully.\n")

    due_date = (datetime.datetime.now() + datetime.timedelta(days=1)).isoformat() + 'Z'
    print("\nTest 2: Adding a task with a due date")
    add_task("Test Task 2 - With Due Date", due=due_date)
    print(f"Task with due date ({due_date}) added successfully.\n")

    print("\nFinal Check: Listing all tasks after adding test tasks")
    list_tasks()
    print("\nAll tasks listed successfully.")

if __name__ == "__main__":
    test_add_task()