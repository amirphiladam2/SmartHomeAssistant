import serial
import speech_recognition as sr
import pyttsx3
import spacy

# Initialize serial communication with ESP32
try:
    ser = serial.Serial('COM15', 9600)  # Change 'COM15' to your ESP32 port
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Adjust text-to-speech engine properties
engine.setProperty('rate', 170)  # Speed of speech (default is 200)
engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

# Load the spaCy language model
nlp = spacy.load("en_core_web_sm")

# Function to recognize voice commands
def recognize_speech():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="en-US")
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            print("Sorry, my speech service is down.")
            return ""

# Function to process the command using spaCy
def process_command(command):
    doc = nlp(command)
    for token in doc:
        print(f"{token.text} -> {token.dep_} -> {token.head.text}")
    return command  # This is a simple pass-through, but you can add more NLP processing here

# Function to control LEDs based on voice commands
def control_led(command):
    command = process_command(command)
    print(f"Recognized command: {command}")
    response = "Command not recognized"
    if 'turn on the green light' in command:
        ser.write(b'1')
        response = "Turning on Green Light"
    elif 'turn off the green light' in command:
        ser.write(b'2')
        response = "Turning off Green Light"
    elif 'turn on the blue light' in command:
        ser.write(b'3')
        response = "Turning on Blue Light"
    elif 'turn off the blue light' in command:
        ser.write(b'4')
        response = "Turning off Blue Light"
    elif 'turn on the red light' in command:
        ser.write(b'5')
        response = "Turning on Red Light"
    elif 'turn off the red light' in command:
        ser.write(b'6')
        response = "Turning off Red Light"
    elif 'turn on the yellow light' in command:
        ser.write(b'7')
        response = "Turning on Yellow Light"
    elif 'turn off the yellow light' in command:
        ser.write(b'8')
        response = "Turning off Yellow Light"
    elif 'turn on all the lights' in command:
        ser.write(b'9')
        response = "Turning on all the lights"
    elif 'turn off all the lights' in command:
        ser.write(b'10')
        response = "Turning off all the lights"
    engine.say(response)      
    engine.runAndWait()

def initial_greeting():
    engine.say("Hello Amir,How was your day?.I'm your Personal AI  Assistant, how can I help you?")
    engine.runAndWait()

initial_greeting()

while True:
    command = recognize_speech()  
    if command:
        control_led(command)
