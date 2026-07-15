import os, subprocess

PATH = os.getenv('PATH').split(';')
def start_app(path=""):
    if not path:
        return "No path selected."

    path = path.strip('"\"')
    try:
        comando = f'start "" "{path}"'
        command = subprocess.Popen(comando, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
    except Exception as e:
        return e
    return 1

def find_app(app_name=""):
    result = subprocess.run(['where', app_name], shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout
    else:
        return result.stderr