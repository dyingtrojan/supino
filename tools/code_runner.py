import subprocess
def run_command(command = r''):
    try:
        command = subprocess.run(command, shell=True, check=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
    except Exception as e:
        return e
    return 1