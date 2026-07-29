import pyttsx3 as ttspy
import threading

tts = ttspy.init()

def _speak_sync(text=""):
    tts.say(text)
    tts.runAndWait()

def speak(text = ""):
    if not text:
        return
    
    thread = threading.Thread(target=_speak_sync, args=(text, ), daemon=True)
    thread.start()