import os
import json
import tkinter as tk
from tkinter import messagebox

# Task class to represent each task
class Task:
    def __init__(self, description, completed=False):
        self.description = description
        self.completed = completed

    def __repr__(self):
        return f"{'[x]' if self.completed else '[ ]'} {self.description}"

# TaskManager class to handle task operations
class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Load tasks from a file."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                try:
                    data = json.load(file)
                    return [Task(**task) for task in data]
                except json.JSONDecodeError:
                    return []
        return []

    def save_tasks(self):
        """Save tasks to a file."""
        with open(self.filename, 'w') as file:
            json.dump([task.__dict__ for task in self.tasks], file, indent=4)

    def add_task(self, description):
        """Add a new task."""
        task = Task(description)
        self.tasks.append(task)
        self.save_tasks()

    def mark_completed(self, task_index):
        """Mark a task as completed."""
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].completed = True
            self.save_tasks()

    def delete_task(self, task_index):
        """Delete a task."""
        if 0 <= task_index < len(self.tasks):
            task = self.tasks.pop(task_index)
            self.save_tasks()

# GUI Application
class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        
        # Set fullscreen and disable resizing
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", self.toggle_fullscreen)  # Press Escape to exit fullscreen mode

        self.manager = TaskManager()

        # Increase the Listbox size
        self.task_listbox = tk.Listbox(self.root, width=80, height=20, selectmode=tk.SINGLE, font=("Arial", 14))
        self.task_listbox.pack(padx=20, pady=20)

        # Entry for adding new tasks
        self.entry = tk.Entry(self.root, width=60, font=("Arial", 14))
        self.entry.pack(padx=20, pady=5)

        # Buttons with increased size
        self.add_button = tk.Button(self.root, text="Add Task", width=20, height=2, font=("Arial", 14), command=self.add_task)
        self.add_button.pack(padx=20, pady=5)

        self.complete_button = tk.Button(self.root, text="Mark as Completed", width=20, height=2, font=("Arial", 14), command=self.mark_completed)
        self.complete_button.pack(padx=20, pady=5)

        self.delete_button = tk.Button(self.root, text="Delete Task", width=20, height=2, font=("Arial", 14), command=self.delete_task)
        self.delete_button.pack(padx=20, pady=5)

        # Add an Exit button to quit the application
        self.exit_button = tk.Button(self.root, text="Exit", width=20, height=2, font=("Arial", 14), command=self.exit_program)
        self.exit_button.pack(padx=20, pady=5)

        self.refresh_task_list()

    def refresh_task_list(self):
        """Refresh the Listbox with tasks."""
        self.task_listbox.delete(0, tk.END)
        for task in self.manager.tasks:
            self.task_listbox.insert(tk.END, str(task))

    def add_task(self):
        """Add a new task."""
        description = self.entry.get()
        if description:
            self.manager.add_task(description)
            self.entry.delete(0, tk.END)
            self.refresh_task_list()
        else:
            messagebox.showwarning("Input Error", "Please enter a task description.")

    def mark_completed(self):
        """Mark a task as completed."""
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.manager.mark_completed(selected_index)
            self.refresh_task_list()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")

    def delete_task(self):
        """Delete a task."""
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.manager.delete_task(selected_index)
            self.refresh_task_list()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen on Escape key press."""
        current_state = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current_state)
        return "break"

    def exit_program(self):
        """Exit the program."""
        confirm = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if confirm:
            self.root.quit()

# Main program
def main():
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
