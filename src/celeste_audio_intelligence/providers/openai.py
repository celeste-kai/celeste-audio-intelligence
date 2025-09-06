import io
from collections.abc import AsyncIterator
from typing import Any

import openai
from celeste_core import AIResponse, AudioArtifact
from celeste_core.base.audio_client import BaseAudioClient
from celeste_core.config.settings import settings
from celeste_core.enums.capability import Capability
from celeste_core.enums.providers import Provider


class OpenAIAudioClient(BaseAudioClient):
    """OpenAI Audio Client for transcription using Whisper and GPT-4o models."""

    def __init__(self, model: str = "whisper-1", **kwargs: Any) -> None:
        super().__init__(
            model=model,
            capability=Capability.AUDIO_TRANSCRIPTION,
            provider=Provider.OPENAI,
            **kwargs,
        )
        self.client = openai.AsyncOpenAI(api_key=settings.openai.api_key)

    async def generate_content(self, prompt: str, audio_file: AudioArtifact, **kwargs: Any) -> AIResponse:
        """Generate text from an audio file using OpenAI models.

        For Whisper: prompt provides context for better accuracy
        For GPT-4o-transcribe: prompt can guide the transcription output
        """
        # Handle both file path and bytes
        if audio_file.data:
            # Use bytes directly with BytesIO
            audio_buffer = io.BytesIO(audio_file.data)
            audio_buffer.name = "audio.mp3"  # Default filename for OpenAI API
            response = await self.client.audio.transcriptions.create(
                model=self.model,
                file=audio_buffer,
                prompt=prompt,  # Optional context prompt for better accuracy
                **kwargs,
            )
        elif audio_file.path:
            # Use file path
            with open(audio_file.path, "rb") as audio:
                response = await self.client.audio.transcriptions.create(
                    model=self.model,
                    file=audio,
                    prompt=prompt,  # Optional context prompt for better accuracy
                    **kwargs,
                )
        else:
            raise ValueError("AudioArtifact must have either data or path")

        # Return AIResponse object
        return AIResponse(
            content=response.text,
            provider=Provider.OPENAI,
            metadata={
                "model": self.model,
                "prompt_used": prompt,  # Include prompt in metadata for transparency
            },
        )

    async def stream_generate_content(
        self, prompt: str, audio_file: AudioArtifact, **kwargs: Any
    ) -> AsyncIterator[AIResponse]:
        """Whisper doesn't support streaming; returns the full response at once."""

        response = await self.generate_content(prompt, audio_file, **kwargs)
        yield response
