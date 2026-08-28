import json
from pathlib import Path

class TodoTask:
    name_task = ""
    tags = []
    completed = False
    
    def __init__(self, name, tags, completed):
        self.name_task = name
        self.tags = tags
        self.completed = completed

tasks = []
tasks_path = Path(rf"{Path.home()}\AppData\Local\Supino\task.json")
folder = Path(rf"{Path.home()}\AppData\Local\Supino")

def save_tasks():
    global tasks
    if not Path(tasks_path).is_file():
        folder.mkdir(parents=True, exist_ok=True)
    with open(tasks_path, 'w') as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)    

def add_task(name, tag, completed):
    task = TodoTask(name=name, tags=tag, completed=completed)
    tasks.append(task)

def load_tasks():
    global tasks
    if not Path(tasks_path).is_file():
        return 1
    else:
        try:
            with open(tasks_path, 'r') as file:
                _tasks = json.load(file)
            return _tasks
        except (json.JSONDecodeError, FileNotFoundError):
            print("Tasks could not be loaded. Maybe it doesn't exists.")
            return []

def get_tasks():
    global tasks
    return tasks
