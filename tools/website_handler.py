import subprocess

def open_website(url=""):
    """
    Opens an URL on the default system web browser. Use ONLY when asked or needed to open an URL for the user.
    """
    if not r"https://" in url:
        url = fr"https://{url}"
    try:
        process = subprocess.Popen(["start", url], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        stdout, stderr = process.communicate()
        output = stdout
        errors = stderr
        return {
            "url": url,
            "return-code": process.returncode,
            "output": output,
            "errors": errors
        }
    except Exception as e:
        return e