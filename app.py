import os
import time
import pygame
from gtts import gTTS
import streamlit as st
import speech_recognition as sr
from googletrans import LANGUAGES, Translator

# Initialize modules
translator = Translator()
pygame.mixer.init()

# Map language names to codes
language_mapping = {name: code for code, name in LANGUAGES.items()}

def get_language_code(language_name):
    return language_mapping.get(language_name, language_name)

def translator_function(spoken_text, from_language, to_language):
    return translator.translate(spoken_text, src=from_language, dest=to_language)

def text_to_voice(text_data, to_language):
    myobj = gTTS(text=text_data, lang=to_language, slow=False)
    myobj.save("cache_file.mp3")
    pygame.mixer.music.load("cache_file.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.5)
    os.remove("cache_file.mp3")

def main_process(output_placeholder, from_language, to_language):
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        output_placeholder.text("🎙️ Listening...")
        rec.pause_threshold = 1
        audio = rec.listen(source, phrase_time_limit=10)

    try:
        output_placeholder.text("🧠 Recognizing...")
        spoken_text = rec.recognize_google(audio, language=from_language)

        output_placeholder.text(f"🔁 Translating: `{spoken_text}`")
        translated = translator_function(spoken_text, from_language, to_language)
        
        st.success(f"🔊 Translated: {translated.text}")
        text_to_voice(translated.text, to_language)

    except Exception as e:
        st.error(f"Error: {e}")

# ---------------------------
# Streamlit UI
# ---------------------------

st.set_page_config(page_title="Real-Time Language Translator", layout="centered")

st.markdown("<h1 style='text-align:center; color:#3e4bdc;'>🌍 Real-Time Language Translator</h1>", unsafe_allow_html=True)
st.markdown("Translate and speak in real time using your microphone 🎤")

from_language_name = st.selectbox("🎧 Select Source Language:", list(LANGUAGES.values()))
to_language_name = st.selectbox("🗣️ Select Target Language:", list(LANGUAGES.values()))

from_language = get_language_code(from_language_name)
to_language = get_language_code(to_language_name)

if st.button("🎬 Start Translation"):
    placeholder = st.empty()
    main_process(placeholder, from_language, to_language)
