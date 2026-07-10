import ollama
from tools import apps_handler, toast_notification, code_runner
from config import setup, preload
from pathlib import Path
import subprocess


subprocess.run(['cls'], shell=True)
preload.load_settings()

def send_toast(title, body, app_name):
    return toast_notification.send_toast(title, body, model_name)
    
def run_commands(code=r''):
    return code_runner.run_command(code)

def find_app_path(app_name=r''):
    return apps_handler.find_app(app_name)

def start_app(path=r''):
    return apps_handler.start_app(path)


tools = [send_toast, run_commands, start_app, find_app_path]
messages = []
print(preload.settings)
system_prompt = preload.settings['system_prompt']
model_name = preload.settings['model']

if preload.history_path.is_file():
    use_history = input("Há um historico de conversa já existente. Quer usar-lo agora? \n (y/n)")
    if use_history.lower() == 'y':
        messages = preload.load_history()
        messages.append({"role": "user", "content": "Eu voltei."})
    if use_history.lower() == 'n':
        messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Olá!"},
        ]

        anwser = ollama.chat(model=model_name, messages=messages, tools=tools, stream=True)
        content = ""
        print("Bot: ", end='', flush=True)
        for chunk in anwser:
            print(chunk.message.content, end='', flush=True)
            content += chunk.message.content
        print("\n")
        messages.append({"role": "assistant", "content": content})
        preload.add_to_history({"role": "assistant", "content": content})
else:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Hello!"},
    ]

    anwser = ollama.chat(model=model_name, messages=messages, tools=tools, stream=True)
    content = ""
    print("Bot: ", end='', flush=True)
    for chunk in anwser:
        print(chunk.message.content, end='', flush=True)
        content += chunk.message.content
    print("\n")
    messages.append({"role": "assistant", "content": content})
    preload.add_to_history({"role": "assistant", "content": content})

while True:
    content = ""
    question = input("User: ")
    if question.lower() == "quit":
        preload.add_to_history({"role": "user", "content": "Tchau"})
        preload.save_history()
        break
    messages.append({"role": "user", "content": question})
    anwser = ollama.chat(model=model_name, messages=messages, tools=tools, stream=True)
    tool_calls = []
    print("Bot: ", end='', flush=True)
    for chunk in anwser:
        print(chunk.message.content, end='', flush=True)
        content += chunk.message.content
        if chunk.message.tool_calls:
            tool_calls.extend(chunk.message.tool_calls)
    available_functions = {"send_toast": send_toast, "run_commands": run_commands, "start_app": start_app, "find_app_path": find_app_path}
    
    assistant_reply = content
    for tool_call in (tool_calls or []):
        func = available_functions.get(tool_call.function.name)
        if func:
            result = func(**tool_call.function.arguments)
            print(str(result))
            messages.append({"role": "tool", "name": tool_call.function.name, "content": str(result)})
            preload.add_to_history({"role": "tool", "name": tool_call.function.name, "content": str(result)})
            follow_up = ollama.chat(model=model_name, messages=messages, stream=True)
            print("\n")
            print("Bot: ", end='', flush=True)
            response = ""
            for chunk in follow_up:
                print(chunk.message.content, end='', flush=True)
                response += chunk.message.content
            messages.append({"role": "assistant", "content": response})
            preload.add_to_history({"role": "assistant", "content": response})
        else:
            print("Assistant (initial):", assistant_reply)
            preload.add_to_history({"role": "assistant", "content": response})
    print("\n")