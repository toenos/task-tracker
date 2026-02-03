"""
assignment: https://roadmap.sh/projects/task-tracker
task-cli using argparse
when using argparse, no "while" or "input()" is needed, so this has to change in comparison to the other script.
also when saving the data it has to do this after every cli-task, not when the "while loop" in previous code is exited.
"""

from datetime import datetime
import json
import os
import argparse

FILENAME = "tasks.json"

def load_tasks():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r") as f:
        return json.load(f)
    
def save_tasks(task_list):
    with open(FILENAME, "w") as f:
        json.dump(task_list, f, indent=2)

def get_current_time():
    return datetime.now().isoformat()

def add_task(task_list, description): # description is now an argument given into the function isntead of "input()"
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

def list_tasks(task_list, status=None): # unchanged
    for task in task_list:
        if status is None or task["status"] == status:
            print(f"[{task['id']}] ({task['status']}) {task['description']}")

def update_task(task_list, task_id, new_description):
    for task in task_list:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = get_current_time()
            return True
    return False

def set_status(task_list, task_id, status):
    for task in task_list:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = get_current_time()
            return True
    return False


def delete_task(task_list, task_id):
    for task in task_list:
        if task["id"] == task_id:
            task_list.remove(task)
            return True
    return False

def main():
    parser = argparse.ArgumentParser(description="Task CLI")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    add_p = subparsers.add_parser("add", help="Add a new task")
    add_p.add_argument("description")

    # update
    update_p = subparsers.add_parser("update", help="Update task description")
    update_p.add_argument("id", type=int)
    update_p.add_argument("description")

    # delete
    delete_p = subparsers.add_parser("delete", help="Delete a task")
    delete_p.add_argument("id", type=int)

    # mark-in-progress
    mip_p = subparsers.add_parser("mark-in-progress", help="Mark task as in progress")
    mip_p.add_argument("id", type=int)

    # mark-done
    done_p = subparsers.add_parser("mark-done", help="Mark task as done")
    done_p.add_argument("id", type=int)

    # list
    list_p = subparsers.add_parser("list", help="List tasks")
    list_p.add_argument(
        "status",
        nargs="?",
        choices=["todo", "in-progress", "done"],
        help="Optional status filter"
    )

    args = parser.parse_args()
    task_list = load_tasks()

    if args.command == "add":
        task, task_list = add_task(task_list, args.description)
        save_tasks(task_list)
        print(f"Task added successfully (ID: {task['id']})")

    elif args.command == "update":
        if update_task(task_list, args.id, args.description):
            save_tasks(task_list)
            print("Task updated successfully")
        else:
            print("Task not found")

    elif args.command == "delete":
        if delete_task(task_list, args.id):
            save_tasks(task_list)
            print("Task deleted successfully")
        else:
            print("Task not found")

    elif args.command == "mark-in-progress":
        if set_status(task_list, args.id, "in-progress"):
            save_tasks(task_list)
            print("Task marked as in-progress")
        else:
            print("Task not found")

    elif args.command == "mark-done":
        if set_status(task_list, args.id, "done"):
            save_tasks(task_list)
            print("Task marked as done")
        else:
            print("Task not found")

    elif args.command == "list":
        if args.status:
            list_tasks(task_list, args.status)
        else:
            list_tasks(task_list)

if __name__ == "__main__":
    main()