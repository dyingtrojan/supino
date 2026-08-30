# this code is literally just a CRUD but for a offline app.
import json
from pathlib import Path

class TodoTask:
    name_task = ""
    tags = []
    completed = False
    
    def __init__(self, id:int, name:str, tags: list, completed:bool = False):
        self.id = id
        self.name_task = name
        self.tags = tags
        self.completed = completed
    
    def to_dict(self):
        return {
            "id": self.id,
            "name_task": self.name_task,
            "tags": self.tags,
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            name=data["name_task"],
            tags=data["tags"],
            completed=data["completed"]
        )

tasks = []
tasks_path = Path(rf"{Path.home()}\AppData\Local\Supino\task.json")
folder = Path(rf"{Path.home()}\AppData\Local\Supino")

def save_tasks():
    global tasks
    if not Path(tasks_path).is_file():
        folder.mkdir(parents=True, exist_ok=True)
    with open(tasks_path, 'w', encoding='utf-8') as file:
        json.dump([task.to_dict() for task in tasks], file, indent=4, ensure_ascii=False)   

def add_task(name:str, tags: list, completed:bool = False):
    new_id = len(tasks)
    task = TodoTask(id=new_id, name=name, tags=tags, completed=completed)
    try:
        tasks.append(task)
        return f"Task {task.name_task} added succesfully with ID {task.id - 1}."
    except Exception as e:
        return e

def load_tasks():
    global tasks
    if not Path(tasks_path).is_file():
        tasks = []
        return []
    else:
        try:
            with open(tasks_path, 'r', encoding="utf-8") as file:
                data = json.load(file)
                tasks = [TodoTask.from_dict(item) for item in data]
            return tasks
        except (json.JSONDecodeError, FileNotFoundError):
            print("Tasks could not be loaded. Maybe it doesn't exist.")
            tasks = []
            return []

def get_tasks():
    global tasks
    string_return = "The following tasks exists: "
    for task in tasks:
        string_return += f"ID: {task.id} | Name: {task.name_task} | Tags: {task.tags} | Completed: {task.completed}"
    return string_return

def find_task_by_id(task_id: int):
    return next((task for task in tasks if task.id == task_id), None)

def find_tasks_by_name(name_query: str):
    return [task for task in tasks if name_query.lower() in task.name_task.lower()]

def complete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            task.completed = True
            return f"Task {task.name_task} (ID: {task.id}) has been completed."
    return None

def remove_task(task_id:int):
    for task in tasks:
        if task.id == task_id:
            tasks.pop(task_id)
            return f"Task {task_id} Removed."
    return None