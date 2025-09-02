import asyncio
from pathlib import Path

import streamlit as st
from celeste_audio_intelligence import create_audio_client
from celeste_audio_intelligence.core.enums import AudioMimeType
from celeste_audio_intelligence.core.types import AudioFile
from celeste_core import Provider, list_models
from celeste_core.enums.capability import Capability


async def main() -> None:
    st.set_page_config(
        page_title="Celeste Audio Intelligence", page_icon="🎵", layout="wide"
    )
    st.title("🎵 Celeste Audio Intelligence")

    # Get providers that support audio transcription
    providers = sorted(
        {m.provider for m in list_models(capability=Capability.AUDIO_TRANSCRIPTION)},
        key=lambda p: p.value,
    )

    with st.sidebar:
        st.header("⚙️ Configuration")
        provider = st.selectbox(
            "Provider:", [p.value for p in providers], format_func=str.title
        )
        models = list_models(
            provider=Provider(provider), capability=Capability.AUDIO_TRANSCRIPTION
        )
        model_names = [m.display_name or m.id for m in models]
        selected_idx = st.selectbox(
            "Model:", range(len(models)), format_func=lambda i: model_names[i]
        )
        model = models[selected_idx].id

    st.markdown(f"*Powered by {provider.title()}*")

    # Audio file selection
    file_source = st.radio("Audio Source", ["Upload a file", "Choose from data folder"])
    audio_path = None

    if file_source == "Upload a file":
        uploaded_file = st.file_uploader(
            "Upload audio file", type=["mp3", "wav", "aiff", "m4a", "flac", "ogg"]
        )
        if uploaded_file:
            temp_path = Path(f"temp_{uploaded_file.name}")
            temp_path.write_bytes(uploaded_file.getbuffer())
            audio_path = temp_path
    else:
        data_files = []
        if Path("data").exists():
            data_files = (
                list(Path("data").glob("*.mp3"))
                + list(Path("data").glob("*.wav"))
                + list(Path("data").glob("*.aiff"))
                + list(Path("data").glob("*.m4a"))
                + list(Path("data").glob("*.flac"))
                + list(Path("data").glob("*.ogg"))
            )
        if data_files:
            selected_file = st.selectbox("Choose a file", [f.name for f in data_files])
            audio_path = Path("data") / selected_file
        else:
            st.warning("No audio files found in data directory")

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
            audio_client = create_audio_client(provider=provider, model=model)

            # Detect MIME type based on file extension
            suffix = audio_path.suffix.lower()
            mime_type_map = {
                ".mp3": AudioMimeType.MP3,
                ".wav": AudioMimeType.WAV,
                ".aiff": AudioMimeType.AIFF,
                ".m4a": AudioMimeType.AAC,
                ".flac": AudioMimeType.FLAC,
                ".ogg": AudioMimeType.OGG,
            }
            mime_type = mime_type_map.get(suffix, AudioMimeType.MP3)

            audio_file = AudioFile(file_path=audio_path, mime_type=mime_type.value)

            with st.spinner("Analyzing audio..."):
                response = await audio_client.generate_content(prompt, audio_file)

                st.success("✅ Analysis complete!")
                st.markdown(f"**Response:**\n\n{response.content}")

                # Show metadata
                with st.expander("📊 Details"):
                    st.write(f"**Provider:** {provider}")
                    st.write(f"**Model:** {model}")
                    st.write(f"**Audio File:** {audio_path.name}")
                    st.write(f"**Format:** {mime_type.value}")
                    if response.usage:
                        st.json(response.usage.model_dump())

            # Cleanup temporary file
            if file_source == "Upload a file" and audio_path.exists():
                audio_path.unlink()

    st.markdown("---")
    st.caption("Built with Streamlit • Powered by Celeste")


if __name__ == "__main__":
    asyncio.run(main())
