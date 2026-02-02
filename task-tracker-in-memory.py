"""
assignment: https://roadmap.sh/projects/task-tracker
This script is built as starting out with the assignment before learning about the imports for cli-parsing (e.g. argparse or other modules)
I't mainly focusses on using functions, returning data, using while loop to keep the program running and per-action logic.
After this script i will read into the argparse and other modules that can solve the cli-tracker and save that as task-cli.py
"""

from datetime import datetime
import json
import os

FILENAME = "tasks.json"

def load_tasks():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r") as f:
        return json.load(f)
    
def save_tasks(task_list):
    with open(FILENAME, "w") as f:
        json.dump(task_list, f, indent=2)

# This program is going to need datetime for multiple times (add, update) => DRY principle to not repeat yourself so thats why i created this function)
def get_current_time():
    return datetime.now().isoformat()

def add_task(task_list):
    description = input("what task would you like to add? \n")
    id = len(task_list) + 1
    task = {
        "id": id,
        "description": description,
        "status": "todo",
        "createdAt": get_current_time(),
        "updatedAt": get_current_time(),
    }
    task_list.append(task)
    return task, task_list

def list_tasks(task_list, status=None):
    for task in task_list:
        if status is None or task["status"] == status:
            print(f"[{task['id']}] ({task['status']}) {task['description']}")

def update_task(task_list):
    task_id = int(input("Enter task id to update: "))
    new_status = input("Enter new status (todo/in-progress/done): ")

    for task in task_list:
        if task["id"] == task_id:
            task["status"] = new_status
            task["updatedAt"] = get_current_time()
            print("Task updated.")
            return
    print("Task not found.")

def delete_task(task_list):
    task_id = int(input("Enter task id to delete: "))
    for task in task_list:
        if task["id"] == task_id:
            task_list.remove(task)
            return
    print("Task not found.")

def main():
    task_list = []

    while True:
        print("What would you like to do? type 'add', 'list', 'update', 'delete' or 'exit'")
        user_input = input("").strip().lower()

        if user_input == "add":
            task, task_list = add_task(task_list)
            print(f"Task '{task['description']}' added.")
        elif user_input == "list":
            status_type = input("Type status to filter (todo/done/in-progress) or press enter for all: \n").strip()
            if status_type == "":
                list_tasks(task_list)
            else:
                list_tasks(task_list, status_type)
        elif user_input == "update":
            update_task(task_list)
        elif user_input == "delete":
            delete_task(task_list)
        elif user_input == "exit":
            break
        else:
            print("Unknown command.")

main()