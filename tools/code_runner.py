import subprocess, os

def run_command(command=""):
    if not command.strip():
        return {
            "success": False,
            "error": "EMPTY_COMMAND",
            "message": "No command was provided."
        }

    if command.strip().startswith("sudo"):
        return {
            "success": False,
            "error": "SUDO_PROHIBITED",
            "message": "Running commands with sudo is strictly prohibited."
        }

    try:
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True
        )
        return {
            "success": process.returncode == 0,
            "exit_code": process.returncode,
            "message": f"Command started with PID {process.pid}",
            "completed": True,
        }
    except Exception as e:
        return {
            "success": False,
            "error": type(e).__name__,
            "message": str(e),
            "completed": True
        }

def kill_process(pid):
    try:
        os.kill(pid, 0)
        return "Process {pid} killed sucesfully"
    except OSError:
        return OSError