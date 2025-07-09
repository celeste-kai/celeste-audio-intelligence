from enum import Enum


class AudioMimeType(Enum):
    """MIME type enumeration for audio content type identification."""

    WAV = "audio/wav"
    MP3 = "audio/mp3"
    AIFF = "audio/aiff"
    AAC = "audio/aac"
    OGG = "audio/ogg"
    FLAC = "audio/flac"


class AudioIntelligenceProvider(Enum):
    """AI provider enumeration for audio intelligence support."""

    GOOGLE = "google"
    OPENAI = "openai"


class OpenAIAudioModel(Enum):
    WHISPER = "whisper-1"
    GPT_4O_TRANSCRIBE = "gpt-4o-transcribe"
    GPT_4O_MINI_TRANSCRIBE = "gpt-4o-mini-transcribe"
