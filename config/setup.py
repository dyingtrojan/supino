from pathlib import Path
import ollama
from . import preload

settings_path = Path(rf"{Path.home()}\AppData\Local\Supino\settings.json")
history_path = Path(rf"{Path.home()}\AppData\Local\Supino\history.json")
save_history = ""
model_name = ""
system_prompt = ""
available_models = []
model_list = ollama.list()
settings = {}

def run_setup():
    global model_name, save_history, system_prompt
    while not model_name:
        print("MODELS: ")
        i = 1
        for model in model_list.models:
            available_models.append(model.model)
            print(str(i) + " | " + model.model)
            i += 1
        choose_model = int(input("Choose a model (1 a *): "))
        model_name = available_models[choose_model - 1]
        preload.settings["model"] = model_name
        print(f"Selected Model: {model_name}")

    while not save_history or (save_history.lower() != "y" or save_history.lower() != "n"):
        save_history = input("do you want to save your chat history? (y/n): ")
        if save_history.lower() == "y":
            preload.settings["save_history"] = True
            break
        else:
            preload.settings["save_history"] = False
            break
    while not system_prompt:
        system_prompt = input("Type your system prompt (leave empty for 'You are a helpful and offline assistant, and has acess to the user's local machine. Only use valid CMD (Windows Command Prompt) commands.'): ")
        if not system_prompt:
            system_prompt = "You are a helpful and offline assistant, and has acess to the user's local machine. Only use valid CMD (Windows Command Prompt) commands."
        system_prompt = system_prompt + " You can send toast notification using 'send_toast' function. You can run commands with the 'run_commands' function, and if needed to access the user directory, use %USERPROFILE%. You can use 'find_app_path' to find where apps where located."
        preload.settings["system_prompt"] = system_prompt
        break
    preload.save_settings()
