from typing import Any, AsyncIterator

import openai
from celeste_audio_intelligence.core.types import AudioFile
from celeste_core import AIResponse
from celeste_core.base.audio_client import BaseAudioClient
from celeste_core.config.settings import settings
from celeste_core.enums.capability import Capability
from celeste_core.enums.providers import Provider
from celeste_core.models.registry import supports


class OpenAIAudioClient(BaseAudioClient):
    """OpenAI Audio Client for transcription using Whisper and GPT-4o models."""

    def __init__(self, model: str = "whisper-1", **kwargs: Any) -> None:
        self.client = openai.AsyncOpenAI(api_key=settings.openai.api_key)
        self.model_name = model
        # Non-raising validation; store support state for callers to inspect if needed
        self.is_supported = supports(
            Provider.OPENAI, self.model_name, Capability.AUDIO_TRANSCRIPTION
        )

    async def generate_content(
        self, prompt: str, audio_file: AudioFile, **kwargs: Any
    ) -> AIResponse:
        """Generate text from an audio file using OpenAI models.

        For Whisper: prompt provides context for better accuracy
        For GPT-4o-transcribe: prompt can guide the transcription output
        """
        import io

        # Handle both file path and bytes
        if audio_file.data:
            # Use bytes directly with BytesIO
            audio_buffer = io.BytesIO(audio_file.data)
            audio_buffer.name = audio_file.filename or "audio.mp3"
            response = await self.client.audio.transcriptions.create(
                model=self.model_name,
                file=audio_buffer,
                prompt=prompt,  # Optional context prompt for better accuracy
                **kwargs,
            )
        elif audio_file.file_path:
            # Use file path
            with open(audio_file.file_path, "rb") as audio:
                response = await self.client.audio.transcriptions.create(
                    model=self.model_name,
                    file=audio,
                    prompt=prompt,  # Optional context prompt for better accuracy
                    **kwargs,
                )
        else:
            raise ValueError("AudioFile must have either data or file_path")

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
