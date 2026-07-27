import ollama, subprocess, pyfiglet
from tools import apps_handler, toast_notification, code_runner, website_handler
from config import settings, setup
from pathlib import Path

first_messsage = ""

subprocess.run(['cls'], shell=True)
print(pyfiglet.figlet_format("mace's", font='digital'))
print(pyfiglet.figlet_format("S U P I N O", font='nipples'))
settings.load_settings()

tools = [toast_notification.send_toast, code_runner.run_command, apps_handler.start_app, apps_handler.find_app, website_handler.open_website]
messages = []
system_prompt = settings.settings['system_prompt']
model_name = settings.settings['model']

if settings.history_path.is_file():
    use_history = input("There is an chat history saved. Do you want to proceed this conversation?\n (y/n)")
    if use_history.lower() == 'y' or use_history.lower() == 'yes':
        messages = settings.load_history()
        messages.append({"role": "user", "content": "I'm Back."})
        
    if use_history.lower() == 'n' or use_history.lower() == 'no':
        messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Hi!"},
        ]
else:
    try:
        while not first_messsage:
            first_messsage = input("Type a little text about you, introduce yourself to your AI agent: ")
            settings.add_to_history({"role": "user", "content": first_messsage})
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": first_messsage}
            ]
    except Exception as e:
        print(f"An error occured: {e}")

anwser = ollama.chat(model=model_name, messages=messages, tools=tools, stream=True)
content = ""
print("Bot: ", end='', flush=True)
for chunk in anwser:
    print(chunk.message.content, end='', flush=True)
    content += chunk.message.content
print("\n")
messages.append({"role": "assistant", "content": content})
settings.add_to_history({"role": "assistant", "content": content})

while True:
    content = ""
    question = input("User: ")
    if question.lower() == "quit":
        settings.add_to_history({"role": "user", "content": "Bye!"})
        settings.save_history()
        break
    
    messages.append({"role": "user", "content": question})
    settings.add_to_history({"role": "user", "content": question})
    
    anwser = ollama.chat(model=model_name, messages=messages, tools=tools, stream=True)
    tool_calls = []
    available_functions = {"send_toast": toast_notification.send_toast, "run_commands": code_runner.run_command, "start_app": apps_handler.start_app, "find_app": apps_handler.find_app, "open_website": website_handler.open_website}
    tools_index = 0
    print('\n')
    print("Bot: ", end='', flush=True)
    for chunk in anwser:
        print(chunk.message.content, end='', flush=True)
        content += chunk.message.content
        if chunk.message.tool_calls:
            print('\n')
            print(f"Running tool: {chunk.message.tool_calls}")
            tool_calls.extend(chunk.message.tool_calls)
            func = available_functions.get(tool_calls[tools_index].function.name)
            tool_called = tool_calls[tools_index]
            if func:
                result = func(**tool_called.function.arguments)
                messages.append({"role": "tool", "name": tool_called.function.name, "content": str(result)})
                settings.add_to_history({"role": "tool", "name": tool_called.function.name, "content": str(result)})
                tools_index += 1
    print("\n")
    if tool_calls:
        follow_up = ollama.chat(model=model_name, messages=messages, stream=True)
        print("Bot: ", end='', flush=True)
        response = ""
        for chunk in follow_up:
            print(chunk.message.content, end='', flush=True)
            response += chunk.message.content
        print("\n")
        messages.append({"role": "assistant", "content": response})
        settings.add_to_history({"role": "assistant", "content": response})
    assistant_reply = content
    tools_index = 0
    tool_calls = []