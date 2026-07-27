import json
from pathlib import Path
from . import setup

settings_path = Path(rf"{Path.home()}\AppData\Local\Supino\settings.json")
history_path = Path(rf"{Path.home()}\AppData\Local\Supino\history.json")
folder = Path(rf"{Path.home()}\AppData\Local\Supino")
save_history = ""
model_name = ""
system_prompt = ""
available_models = []
history = []
settings = {}

def load_settings():
    global settings
    if not Path(settings_path).is_file():
        setup.run_setup()
        return 0
    with open(settings_path, 'r') as file:
        settings = json.load(file)
    return settings

def load_history():
    global history
    if not Path(history_path).is_file():
        return 1
    else:
        with open(history_path, 'r') as file:
            history = json.load(file)
            return history

def save_settings():
    global settings
    if not Path(settings_path).is_file():
        folder.mkdir(parents=True, exist_ok=True)
    with open(settings_path, 'w') as file:
        json.dump(settings, file, indent=4, ensure_ascii=False)

def save_history():
    global history
    if not Path(history_path).is_file():
        folder.mkdir(parents=True, exist_ok=True)
    if settings['save_history'] == True:
        with open(history_path, 'w') as file:
            json.dump(history, file, indent=4, ensure_ascii=False)

def add_to_history(messages = {}):
    global history
    history.append(messages)