LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu'
}

import os
import time
from gtts import gTTS
import streamlit as st
import speech_recognition as sr
from google_trans_new import google_translator

# Initialize translator
translator = google_translator()
language_mapping = {name: code for code, name in LANGUAGES.items()}

def get_language_code(language_name):
    return language_mapping.get(language_name, language_name)

def translator_function(spoken_text, from_language, to_language):
    return translator.translate(spoken_text, lang_src=from_language, lang_tgt=to_language)

def text_to_voice_streamlit(text_data, to_language):
    tts = gTTS(text=text_data, lang=to_language, slow=False)
    file_path = "cache_file.mp3"
    tts.save(file_path)

    with open(file_path, "rb") as audio_file:
        st.audio(audio_file.read(), format="audio/mp3")

    os.remove(file_path)

def main_process(output_placeholder, from_language, to_language):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        output_placeholder.text("🎙️ Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source, phrase_time_limit=10)

    try:
        output_placeholder.text("🧠 Recognizing speech...")
        spoken_text = recognizer.recognize_google(audio, language=from_language)
        output_placeholder.text(f"🔁 Translating: `{spoken_text}`")
        translated = translator_function(spoken_text, from_language, to_language)

        st.success(f"✅ Translated Text: {translated.text}")
        text_to_voice_streamlit(translated.text, to_language)

    except Exception as e:
        st.error(f"⚠️ Error: {e}")

# ---------------------------
# Streamlit UI
# ---------------------------

st.set_page_config(page_title="Real-Time Language Translator", layout="centered")
st.markdown("<h1 style='text-align:center; color:#3e4bdc;'>🌍 Real-Time Language Translator</h1>", unsafe_allow_html=True)
st.markdown("🎤 Speak, Translate, and Listen Instantly!")

# Create a dropdown using language names
from_language_name = st.selectbox("🎧 Select Source Language:", list(LANGUAGES.values()))
to_language_name = st.selectbox("🗣️ Select Target Language:", list(LANGUAGES.values()))

# Map language name back to code
language_mapping = {name: code for code, name in LANGUAGES.items()}

from_language = get_language_code(from_language_name)
to_language = get_language_code(to_language_name)

if st.button("🎬 Start Translation"):
    placeholder = st.empty()
    main_process(placeholder, from_language, to_language)
