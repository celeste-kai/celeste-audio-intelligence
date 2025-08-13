import asyncio
from pathlib import Path

import streamlit as st
from celeste_audio_intelligence import create_audio_client
from celeste_audio_intelligence.core.enums import AudioMimeType
from celeste_audio_intelligence.core.types import AudioFile
from celeste_core import Provider, list_models
from celeste_core.enums.capability import Capability
from celeste_core.models.registry import list_models as list_models_core

st.title("🎵 Audio Intelligence")

# Sidebar
providers = sorted(
    {m.provider for m in list_models_core(capability=Capability.AUDIO_TRANSCRIPTION)},
    key=lambda p: p.value,
)
provider = st.sidebar.selectbox("Provider", [p.value for p in providers])
models = list_models(
    provider=Provider(provider), capability=Capability.AUDIO_TRANSCRIPTION
)
display = [m.display_name or m.id for m in models]
id_by_display = {d: models[i].id for i, d in enumerate(display)}
selected_display = st.sidebar.selectbox("Model", display)
model_value = id_by_display[selected_display]

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
    audio_client = create_audio_client(provider=provider, model=model_value)
    audio_file = AudioFile(file_path=audio_path, mime_type=AudioMimeType.MP3.value)
    response = asyncio.run(audio_client.generate_content(prompt, audio_file))
    st.write(response.content)

    if file_source == "Uploader un fichier" and audio_path.exists():
        audio_path.unlink()
