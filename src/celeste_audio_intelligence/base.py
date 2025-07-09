from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, Optional

from celeste_client import AIResponse
from celeste_client.core.types import AIUsage

from .core.types import AudioFile


class BaseAudioClient(ABC):
    @abstractmethod
    def __init__(self, **kwargs: Any) -> None:
        """
        Initializes the audio client, loading credentials from the environment.
        Provider-specific arguments can be passed via kwargs.
        """
        pass

    @abstractmethod
    async def generate_content(
        self, prompt: str, audio_file: AudioFile, **kwargs: Any
    ) -> AIResponse:
        """Generates a single response."""
        pass

    @abstractmethod
    def stream_generate_content(
        self, prompt: str, audio_file: AudioFile, **kwargs: Any
    ) -> AsyncIterator[AIResponse]:
        """Streams the response chunk by chunk."""
        pass

    @abstractmethod
    def format_usage(self, usage_data: Any) -> Optional[AIUsage]:
        """Convert provider-specific usage data to standardized AIUsage format."""
        pass
