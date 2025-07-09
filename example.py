import asyncio
from pathlib import Path

import streamlit as st
from celeste_client.core.enums import GeminiModel

from src.celeste_audio_intelligence import create_audio_client
from src.celeste_audio_intelligence.core.enums import (
    AudioIntelligenceProvider,
    AudioMimeType,
    OpenAIAudioModel,
)
from src.celeste_audio_intelligence.core.types import AudioFile

st.title("🎵 Audio Intelligence")

# Sidebar
provider = st.sidebar.selectbox("Provider", [p.name for p in AudioIntelligenceProvider])
model_value = None
if provider == "OPENAI":
    model = st.sidebar.selectbox("Model", [m.name for m in OpenAIAudioModel])
    model_value = OpenAIAudioModel[model].value
elif provider == "GOOGLE":
    model = st.sidebar.selectbox("Model", [m.name for m in GeminiModel])
    model_value = GeminiModel[model].value

file_source = st.radio(
    "Source", ["Uploader un fichier", "Choisir depuis le dossier data"]
)
audio_path = None

if file_source == "Uploader un fichier":
    uploaded_file = st.file_uploader("Upload audio file", type=["mp3", "wav", "aiff"])
    if uploaded_file:
        temp_path = Path(f"temp_{uploaded_file.name}")
        temp_path.write_bytes(uploaded_file.getbuffer())
        audio_path = temp_path
else:
    data_files = (
        list(Path("data").glob("*.mp3"))
        + list(Path("data").glob("*.wav"))
        + list(Path("data").glob("*.aiff"))
    )
    if data_files:
        selected_file = st.selectbox("Choisir un fichier", [f.name for f in data_files])
        audio_path = Path("data") / selected_file

prompt = st.text_area(
    "Prompt", value="Generate a detailed transcript of the audio file."
)

if st.button("Analyze") and audio_path:
    audio_client = create_audio_client(
        provider=AudioIntelligenceProvider[provider].value, model=model_value
    )
    audio_file = AudioFile(file_path=audio_path, mime_type=AudioMimeType.MP3.value)
    response = asyncio.run(audio_client.generate_content(prompt, audio_file))
    st.write(response.content)

    if file_source == "Uploader un fichier" and audio_path.exists():
        audio_path.unlink()
