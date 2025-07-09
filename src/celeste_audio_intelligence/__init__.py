"""
Celeste Audio Intelligence Client.
"""

from typing import Any

__version__ = "0.1.0"

from src.celeste_audio_intelligence.base import BaseAudioClient
from src.celeste_audio_intelligence.core.enums import AudioIntelligenceProvider

SUPPORTED_PROVIDERS = [
    "google",
    "openai",
    "kyutai",
    "huggingface",
]


def create_audio_client(provider: str, **kwargs: Any) -> BaseAudioClient:
    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError(f"Unsupported provider: {provider}")

    if provider == "google":
        from .providers.google import GoogleAudioClient

        return GoogleAudioClient(**kwargs)

    if provider == "openai":
        from .providers.openai import OpenAIAudioClient

        return OpenAIAudioClient(**kwargs)

    raise ValueError(f"Audio Provider {provider} not implemented")


__all__ = [
    "create_audio_client",
    "BaseAudioClient",
    "AudioIntelligenceProvider",
]
