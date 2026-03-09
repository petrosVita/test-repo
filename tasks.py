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


def add_task(title, priority="medium", due_date=None):
    tasks = load_tasks()
    task = {"id": len(tasks) + 1, "title": title, "done": False, "priority": priority, "due_date": due_date}
    tasks.append(task)
    save_tasks(tasks)
    due = f", due: {due_date}" if due_date else ""
    print(f"Added: [{task['id']}] {title} (priority: {priority}{due})")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks.")
        return
    for t in tasks:
        status = "x" if t["done"] else " "
        priority = t.get("priority", "medium")
        due = f" due:{t['due_date']}" if t.get("due_date") else ""
        print(f"[{status}] {t['id']}. {t['title']} [{priority}]{due}")


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
        priority = "medium"
        due_date = None
        remaining = args[1:]
        for flag in ("--priority", "--due"):
            if flag in remaining:
                idx = remaining.index(flag)
                val = remaining[idx + 1]
                remaining = remaining[:idx] + remaining[idx + 2:]
                if flag == "--priority":
                    priority = val
                else:
                    due_date = val
        add_task(" ".join(remaining), priority, due_date)
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
