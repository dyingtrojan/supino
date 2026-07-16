import subprocess
def run_command(command = r''):
    """
    Run commands by the PC terminal. Use this ONLY when the user asks for accesing user files AND with proceed with extreme preucation.
    """
    try:
        command = subprocess.run(command, shell=True, check=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
    except Exception as e:
        return e
    return 1