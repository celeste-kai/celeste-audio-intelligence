from typing import Any, AsyncIterator

import openai
from celeste_audio_intelligence.core.types import AudioFile
from celeste_core import AIResponse, Provider
from celeste_core.base.audio_client import BaseAudioClient
from celeste_core.config.settings import settings
from celeste_core.enums.capability import Capability
from celeste_core.enums.providers import Provider as CoreProvider
from celeste_core.models.registry import supports


class OpenAIAudioClient(BaseAudioClient):
    """OpenAI Audio Client for transcription using Whisper and GPT-4o models."""

    def __init__(self, model: str = "whisper-1", **kwargs: Any) -> None:
        self.client = openai.AsyncOpenAI(api_key=settings.openai.api_key)
        self.model_name = model
        if not supports(
            CoreProvider.OPENAI, self.model_name, Capability.AUDIO_TRANSCRIPTION
        ):
            raise ValueError(
                f"Model '{self.model_name}' does not support AUDIO_TRANSCRIPTION"
            )

    async def generate_content(
        self, prompt: str, audio_file: AudioFile, **kwargs: Any
    ) -> AIResponse:
        """Generate text from an audio file using OpenAI models.

        For Whisper: prompt provides context for better accuracy
        For GPT-4o-transcribe: prompt can guide the transcription output
        """

        with open(audio_file.file_path, "rb") as audio:
            response = await self.client.audio.transcriptions.create(
                model=self.model_name,
                file=audio,
                prompt=prompt,  # Optional context prompt for better accuracy
                **kwargs,
            )

        # Return AIResponse object
        return AIResponse(
            content=response.text,
            provider=Provider.OPENAI,
            metadata={
                "model": self.model_name,
                "prompt_used": prompt,  # Include prompt in metadata for transparency
            },
        )

    async def stream_generate_content(
        self, prompt: str, audio_file: AudioFile, **kwargs: Any
    ) -> AsyncIterator[AIResponse]:
        """Whisper doesn't support streaming; returns the full response at once."""

        response = await self.generate_content(prompt, audio_file, **kwargs)
        yield response
