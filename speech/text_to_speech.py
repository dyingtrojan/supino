import pyttsx3 as ttspy

def speak(text = ""):
    tts = ttspy.init()
    print("Speaking...")
    tts.say(text)
    tts.runAndWait()