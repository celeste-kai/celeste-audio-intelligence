<div align="center">

# 🎧 Celeste Audio Intelligence

### Advanced Audio Processing and Analysis - Transcribe and Analyze Audio

[![Python](https://img.shields.io/badge/Python-3.13+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Providers](https://img.shields.io/badge/Providers-2_Implemented-orange?style=for-the-badge&logo=google&logoColor=white)](#-supported-providers)
[![Formats](https://img.shields.io/badge/Audio_Formats-MP3_WAV_FLAC-purple?style=for-the-badge&logo=files&logoColor=white)](#-supported-formats)

[![Demo](https://img.shields.io/badge/🚀_Try_Demo-Jupyter-F37626?style=for-the-badge)](example.py)
[![Documentation](https://img.shields.io/badge/📚_Docs-Coming_Soon-blue?style=for-the-badge)](#)

</div>

---

## 🎯 Why Celeste Audio Intelligence?

<div align="center">
  <table>
    <tr>
      <td align="center">🔌<br><b>Unified API</b><br>One interface for all audio AI providers</td>
      <td align="center">🎧<br><b>Multi-Format</b><br>MP3, WAV, FLAC, & more</td>
      <td align="center">⚡<br><b>Async First</b><br>Built for performance</td>
      <td align="center">🌊<br><b>Streaming</b><br>Real-time response streaming</td>
    </tr>
  </table>
</div>

## 🚀 Quick Start

```python
# Install
!uv add celeste-audio-intelligence  # Coming soon to PyPI

# Process audio with AI
from celeste_audio_intelligence import create_audio_client
from celeste_audio_intelligence.core.enums import AudioMimeType
from celeste_core import AudioArtifact

# Create a client (Google Gemini is implemented)
client = create_audio_client("google", model="gemini-2.5-flash")

# Create an audio file reference
audio_file = AudioArtifact(
    path="audio.mp3",
    mime_type=AudioMimeType.MP3.value
)

# Ask questions about the audio
response = await client.generate_content(
    prompt="Summarize this audio",
    audio_file=audio_file
)

print(response.text)  # AI-generated summary
# Usage accounting is temporarily removed and will be reintroduced later
```

## 📦 Installation

<details open>
<summary><b>Using UV (Recommended)</b></summary>

```bash
git clone https://github.com/yourusername/celeste-audio-intelligence
cd celeste-audio-intelligence
uv sync
```
</details>

<details>
<summary><b>Using pip</b></summary>

```bash
git clone https://github.com/yourusername/celeste-audio-intelligence
cd celeste-audio-intelligence
pip install -e .
```
</details>

## 🔧 Configuration

### 1️⃣ Create your environment file
```bash
cp .env.example .env
```

### 2️⃣ Add your API keys

<details>
<summary><b>🔑 API Key Setup</b></summary>

| Provider | Environment Variable | Get API Key |
|----------|---------------------|-------------|
| 🌈 **Gemini** | `GOOGLE_API_KEY` | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| 🤖 **OpenAI** | `OPENAI_API_KEY` | [OpenAI Platform](https://platform.openai.com/api-keys) |
| 🌊 **Mistral** | `MISTRAL_API_KEY` | [Mistral Console](https://console.mistral.ai/) |
| 🎭 **Anthropic** | `ANTHROPIC_API_KEY` | [Anthropic Console](https://console.anthropic.com/) |
| 🤗 **Hugging Face** | `HUGGINGFACE_TOKEN` | [HF Settings](https://huggingface.co/settings/tokens) |
| 🦙 **Ollama** | *No key needed!* | [Install Ollama](https://ollama.com/download) |

</details>

## 🎨 Supported Providers

<div align="center">

| Provider | Status | Models | Batch Processing | Free Tier |
|----------|--------|--------|-----------------|------------|
| 🌈 **Google** | ✅ Implemented | 3 | ✅ | ✅ |
| 🤖 **OpenAI** | ✅ Implemented | 2 | ✅ | ❌ |
| 🌊 **Mistral AI** | 🛠️ Planned | - | - | ✅ |
| 🎭 **Anthropic** | 🛠️ Planned | - | - | ❌ |
| 🤗 **Hugging Face** | 🛠️ Planned | - | - | ✅ |
| 🦙 **Ollama** | 🛠️ Planned | - | - | ✅ |

</div>

## 📊 Supported Audio Formats

<details>
<summary><b>View All Formats</b></summary>

### 🎧 Audio
- **MP3** - MPEG Audio Layer III
- **WAV** - Waveform Audio File Format
- **FLAC** - Free Lossless Audio Codec
- **AAC** - Advanced Audio Coding
- **OGG** - Ogg Vorbis
- **AIFF** - Audio Interchange File Format

### 💻 Code
- **Python** (.py)
- **JavaScript** (.js)
- **CSS** (.css)
- **Markdown** (.md)

### 🌈 AI Models (Currently Implemented)
- **Gemini 2.5 Flash Lite** - Fast, lightweight model
- **Gemini 2.5 Flash** - Balanced performance
- **Gemini 2.5 Pro** - Highest capability
- **OpenAI Whisper** - Transcription model
- **OpenAI GPT-4o Transcribe** - Advanced transcription

</details>

## 🎮 Interactive Demo

Try our Python example: [example.py](example.py)

Or run the Streamlit app:
```bash
streamlit run example.py
```

## 🗺️ Roadmap

### Celeste-Audio-Intelligence Next Steps
- [x] 📝 **Core Types** - AudioArtifact and AIResponse
- [ ] 📊 **Usage Accounting** - Deferred; will be reintroduced later across modalities
- [x] 🌈 **Google Provider** - Gemini 2.5 models implementation
- [x] 🤖 **OpenAI Provider** - Whisper and GPT-4o support
- [ ] 🌊 **Mistral Provider** - Audio intelligence models
- [ ] 🎭 **Anthropic Provider** - Claude 3 audio capabilities
- [ ] 🧪 **Unit Tests** - Comprehensive test coverage
- [ ] 📚 **Documentation** - API documentation with examples
- [ ] 📦 **PyPI Package** - Publish to PyPI as `celeste-audio-intelligence`

### Celeste Ecosystem

| Package | Description | Status |
|---------|-------------|--------|
| 🎧 **celeste-audio-intelligence** | Audio processing and analysis | 🔄 This Package |
| 📄 **celeste-document-intelligence** | PDF and document processing | ✅ Available |
| 💬 **celeste-client** | Text generation and chat | ✅ Available |
| 💬 **celeste-conversations** | Multi-turn conversations with memory | 🔄 In Progress |
| 🌐 **celeste-web-agent** | Web browsing and automation | 📋 Planned |
| 🎨 **celeste-image-generation** | Image generation across providers | 📋 Planned |
| 🖼️ **celeste-image-intelligence** | Image analysis and understanding | 📋 Planned |
| 🌟 **celeste-embeddings** | Text embeddings across providers | 📋 Planned |
| 📈 **celeste-table-intelligence** | Excel, CSV, and Parquet analysis | 📋 Planned |
| 🎥 **celeste-video-intelligence** | Video analysis and understanding | 📋 Planned |
| 🚀 **And many more...** | Expanding ecosystem of AI tools | 🔮 Future |

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  Made with ❤️ by the Celeste Team
  
  <a href="#-celeste-audio-intelligence">⬆ Back to Top</a>
</div>