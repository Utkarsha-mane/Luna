import speech_recognition as sr
import webbrowser
import pyttsx3
from huggingface_hub import InferenceClient

# Initialize speech recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Hugging Face API and model
HF_API_TOKEN = "Your HF token"
MODEL = "mistralai/Mistral-7B-Instruct-v0.1"  
client = InferenceClient(token=HF_API_TOKEN, model=MODEL)


engine.setProperty('voice', voices[1].id)

# Music dictionary
music = {
    "onthefloor": "https://youtu.be/t4H_Zoh7G5A",
    "chaarkadam": "https://youtu.be/WKbwopSXLWU",
    "neverending story": "https://youtu.be/O5HQ1sZseKg",
    "fearless": "https://youtu.be/7lLigiVgJsE",
    "runaway": "https://youtu.be/d_HlPboLRL8"
}

# Speak function
def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# Process command
def processCommand(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open whatsapp" in c:
        webbrowser.open("https://web.whatsapp.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif "photos" in c:
        webbrowser.open(r"C:\\Pictures\\Saved Pictures\\resume photo - Shortcut.lnk")
    elif c.startswith("play"):
        song = c.replace("play", "").strip()
        if song in music:
            webbrowser.open(music[song])
        else:
            speak("Sorry, I don't have that song.")
    else:
        response = client.text_generation(prompt=c, max_new_tokens=100)
        speak(response.strip())

# Main loop
if __name__ == "__main__":
    speak("Hello dear, I'm Luna. How may I help you?")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
                wake_word = recognizer.recognize_google(audio)

            if "unknown" in wake_word.lower():
                speak("Yes?")
                with sr.Microphone() as source:
                    print("Listening for command...")
                    command_audio = recognizer.listen(source, timeout=5)
                    command = recognizer.recognize_google(command_audio)
                    print(f"Command: {command}")
                    processCommand(command)

        except sr.UnknownValueError:
            print("Couldn't understand. Please try again.")
        except sr.RequestError:
            speak("Sorry, speech service is down.")
        except Exception as e:
            print(f"Error: {str(e)}")
