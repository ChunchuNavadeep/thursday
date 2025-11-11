from bs4 import BeautifulSoup
import speech_recognition as sr
import webbrowser
import pyttsx3
from gtts import gTTS
import pygame
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



recognizer = sr.Recognizer()
engine = pyttsx3.init() 

newsapi = "<Your Key Here>"  # Optional if you want to include news functionality

# API Key for OpenWeatherMap
weather_api_key = "<Your OpenWeatherMap API Key>"

# Global Variables
reminders = []  # List to hold reminder

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

# Email Function (Not Fully Integrated)
def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('youremail@gmail.com', 'your-password')
        server.sendmail('youremail@gmail.com', to, content)
        server.close()
        speak("Email has been sent!")
    except Exception as e:
        speak("Sorry, I couldn't send the email.")
        print(e)

# Weather Function
def get_weather(city):
    complete_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        main_data = data["main"]
        weather_data = data["weather"][0]
        temperature = main_data["temp"]
        humidity = main_data["humidity"]
        description = weather_data["description"]

        weather_report = f"The temperature in {city} is {temperature}°C with {humidity}% humidity. Weather is {description}."
        speak(weather_report)
        print(weather_report)
    else:
        speak("City not found.")
        print("City not found")

# Set Reminders Function
def set_reminder(time_str, reminder_message):
    reminder_time = datetime.datetime.strptime(time_str, "%H:%M")
    reminders.append((reminder_time, reminder_message))
def wishme():
    hour = int(datetime.datetime.now().hour)
    if 0<=hour<12:
        speak("Good Morning sir") 
    elif hour>=12 and hour<17:
        speak("Good Afternoon sir")
    else:
        speak("Good Evening sir")
    speak("I'm thursday , how can i help you")
def check_reminders():
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        for reminder in reminders:
            if current_time == reminder[0].strftime("%H:%M"):
                speak(f"Reminder: {reminder[1]}")
                reminders.remove(reminder)
        time.sleep(60)

# Jokes Function
jokes = [
    "Why don’t skeletons fight each other? They don’t have the guts.",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "Why don’t programmers like nature? It has too many bugs.",
    "What do you call fake spaghetti? An impasta."
]

def tell_joke():
    joke = random.choice(jokes)
    speak(joke)
    print(joke)

# Play Music Function
def play_music(song_name):
    query = '+'.join(song_name.split())
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

# Translate Text Function
def translate_text(text, lang='en'):
    translator = Translator()
    translation = translator.translate(text, dest=lang)
    speak(f"Translated: {translation.text}")
    print(translation.text)

# Task Scheduling (Periodic Task Example)
def job():
    speak("It's time to take a break!")
    print("It's time to take a break!")

schedule.every(30).minutes.do(job)
def searchGoogle(query):
    """Search for a query on Google and read out the top result."""
    # Remove the word "search" from the query
    query = query.replace("search", "").strip()
    
    if query:
        # Perform the Google search
        search_url = f"https://www.google.com/search?q={query}"
        speak(f"Searching for {query} on Google...")
        
        # Send a GET request to Google
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(search_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the page with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract the first search result
            first_result = soup.find('h3')
            
            if first_result:
                result_text = first_result.get_text()
                speak(f"Here is what I found: {result_text}")
                print(f"Google search result: {result_text}")
            else:
                speak("I couldn't find any results on Google.")
        else:
            speak("Sorry, I couldn't perform the search.")
    else:
        speak("Please provide a search query.")
# Command Processing
def processCommand(query):
    query = query.lower()

    # Wikipedia Search
    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
    elif "search " in query.lower():
            query=query.replace("thursday","").strip()
            searchGoogle(query)

    # Open Websites
    elif "open google" in query:
        webbrowser.open("https://google.com")
    elif "open facebook" in query:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in query:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in query:
        webbrowser.open("https://linkedin.com")

    # Current Time
    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")    
        speak(f"Sir, the time is {strTime}")

    elif 'how are you' in query:
        speak("I'm doing well, thank you for asking! How about you?")

    elif 'tell me a joke' in query:
       speak("Why don't scientists trust atoms? Because they make up everything!")

    

  
    # Send Email
    elif 'email to me' in query:
        try:
            speak("What should I say?")
            with sr.Microphone() as source:
                content = r.recognize_google(r.listen(source)) # type: ignore
            to = "name@gmail.com"    
            sendEmail(to, content)
        except Exception as e:
            print(e)
            speak("Sorry sir!, I am not able to send this email") 

    # Weather
    elif "weather" in query:
        speak("Which city do you want the weather for?")
        with sr.Microphone() as source:
            print("Listening for city name...")
            audio = recognizer.listen(source)
            city_name = recognizer.recognize_google(audio)
            get_weather(city_name)

    # Set Reminder
    elif "set reminder" in query:
        speak("What time should I remind you?")
        with sr.Microphone() as source:
            print("Listening for time...")
            audio = recognizer.listen(source)
            time_str = recognizer.recognize_google(audio)

        speak("What is the reminder message?")
        with sr.Microphone() as source:
            print("Listening for reminder message...")
            audio = recognizer.listen(source)
            reminder_message = recognizer.recognize_google(audio)

        set_reminder(time_str, reminder_message)
        speak(f"Reminder set for {time_str} to {reminder_message}")

    # Tell Joke
    elif "tell me a joke" in query:
        tell_joke()

    # Play Music
    elif "play" in query:
        song_name = query.replace("play", "").strip()
        play_music(song_name)

    # Translate Text
    elif "translate" in query:
        speak("What would you like to translate?")
        with sr.Microphone() as source:
            print("Listening for text to translate...")
            audio = recognizer.listen(source)
            text_to_translate = recognizer.recognize_google(audio)

        speak("Which language would you like to translate to?")
        with sr.Microphone() as source:
            print("Listening for language...")
            audio = recognizer.listen(source)
            language = recognizer.recognize_google(audio).lower()

        lang_map = {"spanish": "es", "french": "fr", "german": "de", "english": "en"}
        target_lang = lang_map.get(language, 'en')
        translate_text(text_to_translate, target_lang)

if __name__ == "__main__":
    speak("Initializing Thursday....")
    
    # Start the reminder checking in a background thread
    threading.Thread(target=check_reminders, daemon=True).start()
    wishme()
    while True:
        schedule.run_pending()
        # Listen for the wake word "Thursday"
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.pause_threshold = 1
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            word = recognizer.recognize_google(audio)
            if word.lower() == "thursday":
                speak("Ya")
                # Listen for the command after "Thursday"
                with sr.Microphone() as source:
                    print("Thursday Active...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)
                    

        except Exception as e:
            print("Error; {0}".format(e))
