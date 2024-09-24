#This code implements simple functions to control bulbs and answer few predefined querries.
import serial 
import os
import pygame
import glob
import pyttsx3
import speech_recognition as sr
import pyautogui
import time
import urllib.parse
import webbrowser
import spacy
import serial

# Initialize Serial communication with ESP32
try:
    esp32 = serial.Serial('COM12', 9600)  # Adjust port and baudrate as to your need,for my case my COM PORT is 12 and a baudrate of 9600.
except serial.SerialException as e:
    print(f"Error connecting to ESP32: {e}")
    esp32 = None

# Initialize Spacy NLP
nlp = spacy.load('en_core_web_sm')

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 160)

def speak(audio):
    """Converts text to speech using pyttsx3."""
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    """Listens to user input and converts it to text."""
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
    except Exception as e:
        print(f"Microphone access error: {e}")
        speak("Sorry, I couldn't access the microphone.")
        return "None"
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-us')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        speak("Say that again please...")
        return "None"
    except sr.RequestError as e:
        print(f"Error with Google Speech Recognition service: {e}")
        speak("Sorry, I couldn't reach Google's speech service.")
        return "None"
    
    return query.lower()

def listen_for_greeting():
    """Waits for the user to greet Optimus before starting command mode."""
    while True:
        query = takeCommand()
        if query != "None":
            if any(greet in query for greet in ['hello optimus', 'hi optimus', 'good morning optimus', 'good afternoon optimus', 'good evening optimus']):
                speak(f"Hello mister Amir! How can I assist you today sir?")
                return True
            else:
                speak("Please greet me by saying 'Hello Optimus'.")

def processNLP(query):
    """Processes the query using NLP and extracts intents dynamically."""
    doc = nlp(query)

    # Light control commands
    if any(keyword in query for keyword in ['turn on', 'activate', 'light up']):
        if 'white' in query:
            return "turn on white light"
        elif 'orange' in query:
            return "turn on orange light"
        elif 'green' in query:
            return "turn on green light"
        elif 'all' in query:
            return "turn on all lights"
    
    if any(keyword in query for keyword in ['turn off', 'deactivate', 'shut']):
        if 'white' in query:
            return "turn off white light"
        elif 'orange' in query:
            return "turn off orange light"
        elif 'green' in query:
            return "turn off green light"
        elif 'all' in query:
            return "turn off all lights"

    # General commands
    if 'what is your name' in query:
        return "name"
    if 'what can you do' in query:
        return "capabilities"
    if 'open youtube' in query:
        return "youtube"
    if 'open google' in query:
        return "google"
    if 'time' in query:
        return "time"
    if 'exit' in query or 'goodbye' in query:
        return "exit"
    
    return "unrecognized"

def control_bulb(command):
    """Controls bulbs by sending serial commands to ESP32."""
    if esp32 is None:
        speak("ESP32 connection is unavailable.")
        return False

    try:
        if command == "turn on white light":
            esp32.write(b'white_on')
            speak("Turning on the white light")
        elif command == "turn off white light":
            esp32.write(b'white_off')
            speak("Turning off the white light")
        elif command == "turn on orange light":
            esp32.write(b'orange_on')
            speak("Turning on the orange light")
        elif command == "turn off orange light":
            esp32.write(b'orange_off')
            speak("Turning off the orange light")
        elif command == "turn on green light":
            esp32.write(b'green_on')
            speak("Turning on the green light")
        elif command == "turn off green light":
            esp32.write(b'green_off')
            speak("Turning off the green light")
        elif command == "turn on all lights":
            esp32.write(b'all_on')
            speak("Turning on all lights")  
        elif command == "turn off all lights":
            esp32.write(b'all_off')
            speak("Turning off all lights")
        else:
            return False
        return True
    except serial.SerialException as e:
        speak("There was a problem with the connection to the ESP32.")
        print(f"Serial communication error: {e}")
        return False

def handleGeneralCommands(command):
    """Handles non-light-related commands."""
    if command == "name":
        speak("My name is Optimus Prime")
        return True
    elif command == "capabilities":
        speak("I can control the lights in your room, play music, open websites, and more!")
        return True
    elif command == "youtube":
        speak("Opening YouTube")
        webbrowser.open("youtube.com")
        return True
    elif command == "google":
        speak("Opening Google")
        webbrowser.open("google.com")
        return True
    elif command == "time":
        strTime = time.strftime("%H:%M:%S")
        speak(f"Sir, the time is {strTime}")
        return True
    elif command == "exit":
        speak("Goodbye!")
        return True
    return False

if __name__ == "__main__":
    # Listen for the greeting to initialize the conversation
    if listen_for_greeting():
        while True:
            query = takeCommand()

            if query == "None":
                continue  # Ignore unrecognized commands

            # Process the command using NLP
            processed_query = processNLP(query)

            if processed_query == "unrecognized":
                speak("Sorry, I didn't understand that command.")
            else:
                # Try handling bulb control first
                if not control_bulb(processed_query):
                    # If not a bulb control command, handle general commands
                    if handleGeneralCommands(processed_query):
                        # Break loop if the 'exit' or 'goodbye' command was issued
                        if processed_query == "exit":
                            break
                    
