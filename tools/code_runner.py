import subprocess

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
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )

        return {
            "success": result.returncode == 0,
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "completed": True
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "TIMEOUT",
            "message": "The command timed out after 30 seconds.",
            "completed": True
        }

    except Exception as e:
        return {
            "success": False,
            "error": type(e).__name__,
            "message": str(e),
            "completed": True
        }
