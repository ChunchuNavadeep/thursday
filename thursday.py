from bs4 import BeautifulSoup
import speech_recognition as sr
import webbrowser
import pyttsx3
import os
import wikipedia
import datetime
import smtplib
import random
import requests
import time
import threading
import schedule
from googletrans import Translator

# Initialize
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# API KEYS
weather_api_key = "YOUR_OPENWEATHER_API_KEY"

# Global Variables
reminders = []

# ---------------- SPEAK FUNCTION ----------------
def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# ---------------- EMAIL FUNCTION ----------------
def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('youremail@gmail.com', 'your_app_password')
        server.sendmail('youremail@gmail.com', to, content)
        server.close()
        speak("Email has been sent!")
    except Exception as e:
        speak("Sorry, I couldn't send the email.")
        print(e)

# ---------------- WEATHER FUNCTION ----------------
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != "404":
        main = data["main"]
        weather = data["weather"][0]

        report = f"Temperature in {city} is {main['temp']}°C with {main['humidity']}% humidity. Weather is {weather['description']}."
        speak(report)
    else:
        speak("City not found")

# ---------------- REMINDER ----------------
def set_reminder(time_str, message):
    reminder_time = datetime.datetime.strptime(time_str, "%H:%M")
    reminders.append((reminder_time, message))

def check_reminders():
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        for r in reminders:
            if now == r[0].strftime("%H:%M"):
                speak(f"Reminder: {r[1]}")
                reminders.remove(r)
        time.sleep(60)

# ---------------- WISH ----------------
def wishme():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good Morning")
    elif hour < 17:
        speak("Good Afternoon")
    else:
        speak("Good Evening")

    speak("I am Thursday. How can I help you?")

# ---------------- JOKES ----------------
def tell_joke():
    jokes = [
        "Why don’t skeletons fight each other? They don’t have the guts.",
        "Why don’t programmers like nature? Too many bugs.",
        "What do you call fake spaghetti? An impasta."
    ]
    joke = random.choice(jokes)
    speak(joke)

# ---------------- MUSIC ----------------
def play_music(song):
    query = song.replace(" ", "+")
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

# ---------------- TRANSLATION ----------------
def translate_text():
    translator = Translator()

    speak("What should I translate?")
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio)

    speak("Which language?")
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        lang = recognizer.recognize_google(audio).lower()

    lang_map = {"spanish": "es", "french": "fr", "german": "de", "english": "en"}
    target = lang_map.get(lang, "en")

    translated = translator.translate(text, dest=target)
    speak(translated.text)

# ---------------- GOOGLE SEARCH ----------------
def search_google(query):
    speak(f"Searching {query}")
    webbrowser.open(f"https://www.google.com/search?q={query}")

# ---------------- COMMAND PROCESSOR ----------------
def processCommand(query):
    query = query.lower()

    if "wikipedia" in query:
        speak("Searching Wikipedia")
        query = query.replace("wikipedia", "")
        result = wikipedia.summary(query, sentences=2)
        speak(result)

    elif "search" in query:
        search_google(query.replace("search", ""))

    elif "open google" in query:
        webbrowser.open("https://google.com")

    elif "open youtube" in query:
        webbrowser.open("https://youtube.com")

    elif "time" in query:
        time_now = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {time_now}")

    elif "joke" in query:
        tell_joke()

    elif "play" in query:
        play_music(query.replace("play", ""))

    elif "weather" in query:
        speak("Which city?")
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            city = recognizer.recognize_google(audio)
        get_weather(city)

    elif "translate" in query:
        translate_text()

    elif "set reminder" in query:
        speak("Tell time in HH:MM format")
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            t = recognizer.recognize_google(audio)

        speak("What reminder?")
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            msg = recognizer.recognize_google(audio)

        set_reminder(t, msg)
        speak("Reminder set")

    elif "exit" in query or "stop" in query:
        speak("Goodbye")
        exit()

# ---------------- MAIN ----------------
if __name__ == "__main__":
    speak("Initializing Thursday")

    threading.Thread(target=check_reminders, daemon=True).start()
    wishme()

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.pause_threshold = 1
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            word = recognizer.recognize_google(audio)

            if "thursday" in word.lower():
                speak("Yes?")

                with sr.Microphone() as source:
                    audio = recognizer.listen(source)

                command = recognizer.recognize_google(audio)
                processCommand(command)

        except Exception as e:
            print("Error:", e)
