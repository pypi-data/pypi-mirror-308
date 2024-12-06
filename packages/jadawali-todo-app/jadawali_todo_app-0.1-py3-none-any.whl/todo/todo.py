# todo.py

# List to store tasks
tasks = []

def add_task(task):
    """Add a new task to the list."""
    tasks.append({"task": task, "completed": False})
    print(f"Added task: '{task}'")

def view_tasks():
    """Display all tasks in the list."""
    if not tasks:
        print("No tasks to display.")
    else:
        print("To-Do List:")
        for index, task in enumerate(tasks, start=1):
            status = "✓" if task["completed"] else "✗"
            print(f"{index}. {task['task']} [{status}]")

def complete_task(task_number):
    """Mark a task as completed by its index."""
    if 0 < task_number <= len(tasks):
        tasks[task_number - 1]["completed"] = True
        print(f"Marked task {task_number} as complete.")
    else:
        print("Invalid task number.")

def main():
    """Main function to interact with the to-do list."""
    while True:
        print("\nOptions: add, view, complete, exit")
        command = input("Enter a command: ").strip().lower()

        if command == "add":
            task = input("Enter a new task: ")
            add_task(task)
        elif command == "view":
            view_tasks()
        elif command == "complete":
            try:
                task_number = int(input("Enter task number to mark as complete: "))
                complete_task(task_number)
            except ValueError:
                print("Please enter a valid number.")
        elif command == "exit":
            print("Goodbye!")
            break
        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()
