import json
import sys
from pathlib import Path

DATA_FILE = Path("tasks.json")


def load_tasks():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return []


def save_tasks(tasks):
    DATA_FILE.write_text(json.dumps(tasks, indent=2))


def add_task(title, priority="medium"):
    tasks = load_tasks()
    task = {"id": len(tasks) + 1, "title": title, "done": False, "priority": priority}
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added: [{task['id']}] {title} (priority: {priority})")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks.")
        return
    for t in tasks:
        status = "x" if t["done"] else " "
        priority = t.get("priority", "medium")
        print(f"[{status}] {t['id']}. {t['title']} [{priority}]")


def mark_done(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save_tasks(tasks)
            print(f"Done: {t['title']}")
            return
    print(f"Task {task_id} not found.")


def remove_task(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    print(f"Removed task {task_id}.")


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: tasks.py <add|list|done|remove> [args]")
        return

    cmd = args[0]
    if cmd == "add" and len(args) > 1:
        # Support: add --priority high <title> or add <title>
        if "--priority" in args:
            idx = args.index("--priority")
            priority = args[idx + 1]
            remaining = args[1:idx] + args[idx + 2:]
            add_task(" ".join(remaining), priority)
        else:
            add_task(" ".join(args[1:]))
    elif cmd == "list":
        list_tasks()
    elif cmd == "done" and len(args) > 1:
        mark_done(int(args[1]))
    elif cmd == "remove" and len(args) > 1:
        remove_task(int(args[1]))
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
