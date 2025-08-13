from enum import Enum


class AudioMimeType(Enum):
    """MIME type enumeration for audio content type identification."""

    WAV = "audio/wav"
    MP3 = "audio/mp3"
    AIFF = "audio/aiff"
    AAC = "audio/aac"
    OGG = "audio/ogg"
    FLAC = "audio/flac"


class OpenAIAudioModel(Enum):
    WHISPER = "whisper-1"
    GPT_4O_TRANSCRIBE = "gpt-4o-transcribe"
    GPT_4O_MINI_TRANSCRIBE = "gpt-4o-mini-transcribe"


class GoogleAudioModel(Enum):
    FLASH_LITE = "gemini-2.5-flash-lite-preview-06-17"
    FLASH = "gemini-2.5-flash"
    PRO = "gemini-2.5-pro"
