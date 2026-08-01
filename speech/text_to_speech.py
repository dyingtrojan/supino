import pyttsx3 as ttspy

tts = ttspy.init()

def speak(text = ""):
    if not text:
        return
    tts.say(text)
    tts.runAndWait()