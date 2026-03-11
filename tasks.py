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


def add_task(title, priority="medium", due_date=None, tags=None, notes=None):
    if tags is None:
        tags = []
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "done": False,
        "priority": priority,
        "due_date": due_date,
        "tags": tags,
        "notes": notes,
    }
    tasks.append(task)
    save_tasks(tasks)
    due = f", due: {due_date}" if due_date else ""
    tag_str = f", tags: {', '.join(tags)}" if tags else ""
    print(f"Added: [{task['id']}] {title} (priority: {priority}{due}{tag_str})")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks.")
        return
    for t in tasks:
        status = "x" if t["done"] else " "
        priority = t.get("priority", "medium")
        due = f" due:{t['due_date']}" if t.get("due_date") else ""
        tags = f" tags:{','.join(t.get('tags', []))}" if t.get("tags") else ""
        notes = f" notes:{t['notes']}" if t.get("notes") else ""
        print(f"[{status}] {t['id']}. {t['title']} [{priority}]{due}{tags}{notes}")


def search_tasks(keyword):
    tasks = load_tasks()
    matches = [t for t in tasks if keyword.lower() in t["title"].lower()]
    if not matches:
        print(f"No tasks matching '{keyword}'.")
        return
    for t in matches:
        status = "x" if t["done"] else " "
        priority = t.get("priority", "medium")
        due = f" due:{t['due_date']}" if t.get("due_date") else ""
        tags = f" tags:{','.join(t.get('tags', []))}" if t.get("tags") else ""
        notes = f" notes:{t['notes']}" if t.get("notes") else ""
        print(f"[{status}] {t['id']}. {t['title']} [{priority}]{due}{tags}{notes}")


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


def clear_tasks():
    save_tasks([])
    print("All tasks cleared.")


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: tasks.py <add|list|done|remove|clear|search> [args]")
        return

    cmd = args[0]
    if cmd == "add" and len(args) > 1:
        priority = "medium"
        due_date = None
        tags = []
        notes = None
        remaining = args[1:]
        i = 0
        while i < len(remaining):
            if remaining[i] == "--priority" and i + 1 < len(remaining):
                priority = remaining[i + 1]
                remaining = remaining[:i] + remaining[i + 2:]
            elif remaining[i] == "--due" and i + 1 < len(remaining):
                due_date = remaining[i + 1]
                remaining = remaining[:i] + remaining[i + 2:]
            elif remaining[i] == "--tag" and i + 1 < len(remaining):
                tags.append(remaining[i + 1])
                remaining = remaining[:i] + remaining[i + 2:]
            elif remaining[i] == "--notes" and i + 1 < len(remaining):
                notes = remaining[i + 1]
                remaining = remaining[:i] + remaining[i + 2:]
            else:
                i += 1
        add_task(" ".join(remaining), priority, due_date, tags, notes)
    elif cmd == "list":
        list_tasks()
    elif cmd == "done" and len(args) > 1:
        mark_done(int(args[1]))
    elif cmd == "remove" and len(args) > 1:
        remove_task(int(args[1]))
    elif cmd == "clear":
        clear_tasks()
    elif cmd == "search" and len(args) > 1:
        search_tasks(" ".join(args[1:]))
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
