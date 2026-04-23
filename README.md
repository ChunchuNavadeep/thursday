# 🎙️ Thursday Voice Assistant

Thursday is a Python-based voice assistant that performs basic tasks like searching the web, telling time, weather updates, reminders, and more using voice commands.

---

## 🚀 Features

* Voice recognition (Speech-to-Text)
* Text-to-speech responses
* Wikipedia search
* Google search
* Weather updates (API-based)
* Reminder system
* Language translation
* Play music via YouTube
* Joke generator
* Wake word activation ("Thursday")

---

## 🛠️ Tech Stack

* Python
* SpeechRecognition
* pyttsx3
* Wikipedia
* Requests
* BeautifulSoup
* Googletrans

---

## 📦 Installation

```bash
pip install speechrecognition pyttsx3 wikipedia requests beautifulsoup4 googletrans==4.0.0-rc1 pyaudio schedule
```

If PyAudio gives error:

```bash
pip install pipwin
pipwin install pyaudio
```

---

## 🔑 Setup

Get a free API key from OpenWeatherMap and add it in the code:

```python
weather_api_key = "YOUR_API_KEY"
```

---

## ▶️ Run

```bash
python main.py
```

---

## 🗣️ Usage

1. Run the program
2. Say **"Thursday"**
3. Give commands like:

* "Search Python"
* "Open YouTube"
* "Tell me a joke"
* "What is the time"
* "Weather"
* "Play song"
* "Translate"
* "Set reminder"

---

## 📁 Structure

```
main.py
README.md
```

---

## 🔮 Future Improvements

* Add AI chatbot (LLM)
* Add GUI (Streamlit)
* Add database for memory

---

## 👤 Author

Navadeep Chunchu
