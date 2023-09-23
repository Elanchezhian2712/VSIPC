import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import datetime
from flask import Blueprint, request, jsonify

voice_command = Blueprint('voice_command', __name__)


engine = None
def initialize_engine():
    global engine
    if engine is None:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)  


def speak(text):
    initialize_engine()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio).lower()
        print("User command:", command)
        return command
    except sr.UnknownValueError:
        speak(f"Sorry, I couldn't understand that.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""


def open_website(url):
    speak(f"Opening {url}")
    webbrowser.open(url)


def read_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}")


def play_music(file_name):
    music_dir = 'E:\\Chaliya Jawan_128-(PagalWorld'  
    file_path = os.path.join(music_dir, file_name)
    if os.path.exists(file_path):
        speak(f"Playing {file_name}")
        os.startfile(file_path)
    else:
        speak(f"Sorry, {file_name} not found in the music directory.")


voice_assistant_active = False

@voice_command.route('/api/voice-command', methods=['POST'])
def handle_voice_command():
    global voice_assistant_active

    data = request.json
    command = data.get('command', '').lower()

    if "start" in command:
        if not voice_assistant_active:
            speak("Voice assistant activated. You can now give voice commands.")
            voice_assistant_active = True
            while voice_assistant_active:
                user_command = listen()
                if "exit" in user_command or "bye" in user_command:
                    speak("Voice assistant deactivated.")
                    voice_assistant_active = False
                elif "open website" in user_command:
                    speak("Please specify the website URL.")
                    website_url = listen()
                    open_website(website_url)
                elif "time" in user_command:
                    read_time()
                elif "open youtube" in user_command:
                    speak("Opening YouTube")
                    webbrowser.open("https://www.youtube.com")
                elif "open google" in user_command:
                    speak("Opening Google")
                    webbrowser.open("https://www.google.com")
                elif "open gmail" in user_command:
                    speak("Opening Gmail")
                    webbrowser.open("https://mail.google.com")
                elif "wikipedia" in user_command:
                    speak('Searching Wikipedia...')
                    user_command = user_command.replace("wikipedia", "")
                    results = wikipedia.summary(user_command, sentences=2)
                    speak("According to Wikipedia")
                    speak(results)
                elif "open stack overflow" in user_command:
                    speak("Opening Stack Overflow")
                    webbrowser.open("https://stackoverflow.com")
                elif "play music" in user_command:
                    speak("Playing music")
                    play_music("Chaliya Jawan_128-(PagalWorld).mp3")
        else:
            speak("Voice assistant is already active.")
    else:
        return jsonify({"response": "Command not recognized."})

    return jsonify({"response": "Voice assistant exited."})
