import ollama
from tools import apps_handler, toast_notification, code_runner, website_handler, todo_list
from speech import text_to_speech
from config import settings
from pathlib import Path
from misc import colors, serialize_to_json

first_messsage = ""
use_history = ""
tools = [toast_notification.send_toast, code_runner.run_command, apps_handler.start_app, apps_handler.find_app, website_handler.open_website, todo_list.get_tasks, todo_list.add_task, todo_list.complete_task, todo_list.find_task_by_id, todo_list.find_tasks_by_name, todo_list.remove_task]

def start_chat():
    global first_messsage, use_history, tools
    
    available_functions = {func.__name__: func for func in tools} # biggest refactoring ever
    
    settings.load_settings()
    todo_list.load_tasks()

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
                if use_history.lower() != 'n' or use_history.lower() != "no":
                    if use_history.lower() == 'y' or use_history.lower() == 'a':
                        if use_history.lower() == 'a':
                            settings.settings["always_load_chat"] == True

                        messages = settings.load_history()
                        messages.append({"role": "user", "content": "I'm Back."})
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
    text_to_speech.speak(content, settings.settings["enable_tts"])
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
            todo_list.save_tasks()
            break
        if question.lower() == "quit":
            settings.add_to_history({"role": "user", "content": "Bye!"})
            settings.save_history()
            todo_list.save_tasks()
            break
        
        messages.append({"role": "user", "content": question})
        settings.add_to_history({"role": "user", "content": question})
        
        while True:
            anwser = ollama.chat(model=model_name, messages=messages, tools=tools, stream=True, think=False)
            tool_calls = []
            
            tools_index = 0
            print('\n')
            print("Bot: ", end='', flush=True)
            
            for chunk in anwser:
                print(chunk.message.content, end='', flush=True)
                content += chunk.message.content
                if chunk.message.tool_calls:
                    tool_calls.extend(chunk.message.tool_calls)
            text_to_speech.speak(content, settings.settings["enable_tts"])
            if tool_calls:
                messages.append({"role": "assistant", "content": content, "tool_calls": serialize_to_json.serialize_tool_calls(tool_calls)})
                history_messages = {
                    "role": "assistant", "content": content
                }
                history_messages["tool_calls"] = [
                    {
                        "function": {
                            "name": tool.function.name,
                            "arguments": tool.function.arguments
                        }
                    }
                    for tool in tool_calls
                ]
                settings.add_to_history(history_messages)
                for tool in tool_calls:
                    func = available_functions.get(tool.function.name)
                    if func:
                        if tool.function.name == "get_task":
                            print(colors.txt_colors["yellow"] + "Loading tasks..." + colors.txt_colors["RESET"])
                        elif tool.function.name == "add_task":
                            print(colors.txt_colors["yellow"] + f"Adding task: {tool.function.arguments["name"]}" + colors.txt_colors["RESET"])
                        else:
                            print(colors.txt_colors["yellow"] + "Running tool: " + colors.txt_colors["RESET"] + tool.function.name)
                            print(colors.txt_colors["yellow"] + "Tool arguments: " + colors.txt_colors["RESET"] + str(tool.function.arguments))

                    result = func(**tool.function.arguments)

                    messages.append({"role": "tool", "name": tool.function.name, "content": str(result)})
                    settings.add_to_history({"role": "tool", "name": tool.function.name, "content": str(result)})
                    tools_index += 1
                continue
            elif tool_calls == []:
                print("\n")
                break