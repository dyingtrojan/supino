from pathlib import Path
import ollama
from . import settings

settings_path = Path(rf"{Path.home()}\AppData\Local\Supino\settings.json")
history_path = Path(rf"{Path.home()}\AppData\Local\Supino\history.json")
save_history = ""
model_name = ""
system_prompt = ""
first_messsage = ""
always_load_history = ''
available_models = []
model_list = ollama.list()


def run_setup():
    global model_name, save_history, system_prompt, first_messsage, always_load_history
    while not model_name:
        print("MODELS: ")
        i = 1
        for model in model_list.models:
            capabilities = ollama.show(model.model).capabilities
            if "tools" in capabilities:    
                available_models.append(model.model)
                print(str(i) + " | " + model.model)
                i += 1
        choose_model = 0
        while choose_model < 0 or choose_model > i or not choose_model:
            try:
                choose_model = int(input("Choose a model (1 a *): "))
            except ValueError:
                choose_model = 0
        model_name = available_models[choose_model - 1]
        settings.settings["model"] = model_name
        print(f"Selected Model: {model_name}")

    while not save_history or (save_history.lower() != "y" or save_history.lower() != "n"):
        save_history = input("Do you want to save your chat history? (y/n): ")
        if save_history.lower() == "y":
            settings.settings["save_history"] = True
            break
        else:
            settings.settings["save_history"] = False
            break
    while not always_load_history:
        always_load_history = input("Do you want to load your chat history everytime you open SUPINO? (y/n/a (ask)): ")
        if always_load_history.lower() == "y":
            settings.settings['always_load_chat'] = True
            break
        if always_load_history.lower() == "n" or always_load_history.lower() == "a":
            settings.settings['always_load_chat'] = False
            break
    while not system_prompt:
        system_prompt = input("Type your system prompt (leave empty for 'You are a helpful and offline assistant, and has acess to the user's local machine. Only use valid CMD (Windows Command Prompt) commands.'): ")
        if not system_prompt:
            system_prompt = "You are a helpful and offline assistant, and has acess to the user's local machine. Only use valid CMD (Windows Command Prompt) commands."
    
        settings.settings["system_prompt"] = system_prompt
        break
    settings.save_settings()
