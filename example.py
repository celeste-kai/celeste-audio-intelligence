import asyncio
from pathlib import Path
from typing import Any

import streamlit as st
from celeste_core import AudioArtifact, Provider, list_models
from celeste_core.enums.capability import Capability

from celeste_audio_intelligence import create_audio_client


def setup_sidebar() -> tuple[str, str]:
    """Setup sidebar configuration and return provider and model."""
    # Get providers that support audio transcription
    providers = sorted(
        {m.provider for m in list_models(capability=Capability.AUDIO_TRANSCRIPTION)},
        key=lambda p: p.value,
    )

    with st.sidebar:
        st.header("⚙️ Configuration")
        provider = str(st.selectbox("Provider:", [p.value for p in providers], format_func=str.title))
        models = list_models(provider=Provider(provider), capability=Capability.AUDIO_TRANSCRIPTION)
        model_names = [m.display_name or m.id for m in models]
        selected_idx = int(st.selectbox("Model:", range(len(models)), format_func=lambda i: model_names[i]))
        model = models[selected_idx].id

    return provider, model


def handle_file_upload() -> Path | None:
    """Handle file upload and return path if successful."""
    uploaded_file = st.file_uploader("Upload audio file", type=["mp3", "wav", "aiff", "m4a", "flac", "ogg"])
    if uploaded_file:
        temp_path = Path(f"temp_{uploaded_file.name}")
        temp_path.write_bytes(uploaded_file.getbuffer())
        return temp_path
    return None


def get_data_files() -> list[Path]:
    """Get available audio files from data directory."""
    if not Path("data").exists():
        return []

    extensions = ["*.mp3", "*.wav", "*.aiff", "*.m4a", "*.flac", "*.ogg"]
    data_files: list[Path] = []
    for ext in extensions:
        data_files.extend(Path("data").glob(ext))
    return data_files


def handle_data_folder_selection() -> Path | None:
    """Handle data folder file selection and return path if successful."""
    data_files = get_data_files()
    if data_files:
        selected_file = st.selectbox("Choose a file", [f.name for f in data_files])
        return Path("data") / str(selected_file)
    else:
        st.warning("No audio files found in data directory")
        return None


def get_audio_file() -> Path | None:
    """Get audio file based on user selection."""
    file_source = st.radio("Audio Source", ["Upload a file", "Choose from data folder"])

    if file_source == "Upload a file":
        return handle_file_upload()
    else:
        return handle_data_folder_selection()


def normalize_audio_format(audio_path: Path) -> str:
    """Normalize audio format name."""
    format_name = audio_path.suffix.lower().lstrip(".")
    if format_name == "m4a":
        format_name = "aac"  # Normalize m4a to aac
    return format_name


def display_results(response: Any, provider: str, model: str, audio_path: Path, format_name: str) -> None:
    """Display analysis results and metadata."""
    st.success("✅ Analysis complete!")
    st.markdown(f"**Response:**\n\n{response.content}")

    # Show metadata
    with st.expander("📊 Details"):
        st.write(f"**Provider:** {provider}")
        st.write(f"**Model:** {model}")
        st.write(f"**Audio File:** {audio_path.name}")
        st.write(f"**Format:** {format_name}")
        if response.metadata:
            st.json(response.metadata)


async def process_audio(provider: str, model: str, prompt: str, audio_path: Path) -> None:
    """Process audio file with the selected provider and model."""
    audio_client = create_audio_client(provider=provider, model=model)
    format_name = normalize_audio_format(audio_path)
    audio_file = AudioArtifact(path=str(audio_path), format=format_name)

    with st.spinner("Analyzing audio..."):
        response = await audio_client.generate_content(prompt, audio_file)
        display_results(response, provider, model, audio_path, format_name)


async def main() -> None:
    st.set_page_config(page_title="Celeste Audio Intelligence", page_icon="🎵", layout="wide")
    st.title("🎵 Celeste Audio Intelligence")

    provider, model = setup_sidebar()
    st.markdown(f"*Powered by {provider.title()}*")

    # Audio file selection
    audio_path = get_audio_file()

    # Prompt input
    prompt = st.text_area(
        "Enter your prompt:",
        "Generate a detailed transcript of the audio file.",
        height=100,
        placeholder="Describe what you want to analyze about the audio...",
    )

    if st.button("🎵 Analyze", type="primary", use_container_width=True):
        if not audio_path:
            st.error("Please select or upload an audio file.")
        elif not prompt.strip():
            st.error("Please enter a prompt.")
        else:
            await process_audio(provider, model, prompt, audio_path)

            # Cleanup temporary file if uploaded
            if audio_path.name.startswith("temp_") and audio_path.exists():
                audio_path.unlink()

    st.markdown("---")
    st.caption("Built with Streamlit • Powered by Celeste")


if __name__ == "__main__":
    asyncio.run(main())
