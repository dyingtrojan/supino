import ollama, subprocess, pyfiglet, random
from tools import apps_handler, toast_notification, code_runner, website_handler
from speech import text_to_speech
from config import settings, setup
from pathlib import Path
from misc import colors, title_text


first_messsage = ""
use_history = ""


def start_chat():
    global first_messsage, use_history
    settings.load_settings()

    tools = [toast_notification.send_toast, code_runner.run_command, apps_handler.start_app, apps_handler.find_app, website_handler.open_website]
    messages = []
    system_prompt = settings.settings['system_prompt']
    model_name = settings.settings['model']

    if settings.history_path.is_file():
        if settings.settings['always_load_chat'] != True or settings.settings["always_load_chat"] != None:
            messages = settings.load_history()
            messages.append({"role": "user", "content": "I'm Back."})
        else:    
            while not use_history:
                use_history = input("There is an chat history saved. Do you want to proceed this conversation?\n (y/n/a (always))")
                if use_history.lower() == 'y' or use_history.lower() == 'yes':
                    messages = settings.load_history()
                    messages.append({"role": "user", "content": "I'm Back."})    
                elif use_history.lower() == 'n' or use_history.lower() == 'no':
                    messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": "Hi!"},
                    ]
                elif use_history.lower() == 'a' or use_history.lower() == 'always':
                    messages = settings.load_history()
                    messages.append({"role": "user", "content": "I'm Back."})
                    settings.settings["always_load_chat"] == True
                else:
                    use_history = ""
            
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
    if settings.settings["tts_enabled"] == True:
        text_to_speech.speak(content)
    messages.append({"role": "assistant", "content": content})
    settings.add_to_history({"role": "assistant", "content": content})

    while True:
        content = ""
        try:
            question = input("User: ")
        except KeyboardInterrupt:
            print("App interrupted by user.")
            settings.add_to_history({"role": "user", "content": "Bye!"})
            settings.save_history()
            break
        if question.lower() == "quit":
            settings.add_to_history({"role": "user", "content": "Bye!"})
            settings.save_history()
            break
        
        messages.append({"role": "user", "content": question})
        settings.add_to_history({"role": "user", "content": question})
        
        anwser = ollama.chat(model=model_name, messages=messages, tools=tools, stream=True, think=False)
        tool_calls = []
        available_functions = {"send_toast": toast_notification.send_toast, "run_commands": code_runner.run_command, "start_app": apps_handler.start_app, "find_app": apps_handler.find_app, "open_website": website_handler.open_website, "open_files": code_runner.open_file}
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
        if settings.settings["tts_enabled"] == True:
            text_to_speech.speak(content)
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
        if settings.settings["tts_enabled"] == True:
            text_to_speech.speak(response)