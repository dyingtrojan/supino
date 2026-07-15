import subprocess
# this gotta be the WORST name i've ever given to a script. i gotta rename it to something better later and i HOPE this happens
def open_website(url=""):
    if not r"https://" in url:
        url = fr"https://{url}"
    try:
        subprocess.Popen(["start", url], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        return 1
    except Exception as e:
        return e