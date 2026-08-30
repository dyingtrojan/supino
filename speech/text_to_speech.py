import pyttsx3 as ttspy

tts = ttspy.init()
def speak(text = "", enabled = False):
    if enabled == False:
        if not text:
                return
        tts.say(text)
        tts.runAndWait()