from typing import Any, AsyncIterator

from celeste_audio_intelligence.core.types import AudioFile
from celeste_core import AIResponse, Provider
from celeste_core.base.audio_client import BaseAudioClient
from celeste_core.config.settings import settings
from celeste_core.enums.capability import Capability
from google import genai


class GoogleAudioClient(BaseAudioClient):
    def __init__(
        self, model: str = "gemini-2.5-flash-lite-preview-06-17", **kwargs: Any
    ) -> None:
        super().__init__(
            model=model,
            capability=Capability.AUDIO_TRANSCRIPTION,
            provider=Provider.GOOGLE,
            **kwargs,
        )
        self.client = genai.Client(api_key=settings.google.api_key)

    async def generate_content(
        self, prompt: str, audio_file: AudioFile, **kwargs: Any
    ) -> AIResponse:
        """Generate text from a prompt and a list of documents."""
        import io

        # Handle both file path and bytes
        if audio_file.data:
            # Upload bytes directly
            audio_buffer = io.BytesIO(audio_file.data)
            audio_buffer.name = audio_file.filename or "audio.mp3"
            audio = await self.client.aio.files.upload(file=audio_buffer)
        elif audio_file.file_path:
            # Upload from file path
            audio = await self.client.aio.files.upload(file=audio_file.file_path)
        else:
            raise ValueError("AudioFile must have either data or file_path")

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=[prompt, audio],
            **kwargs,
        )

        # Return AIResponse object
        return AIResponse(
            content=response.text,
            provider=Provider.GOOGLE,
            metadata={"model": self.model},
        )

    async def stream_generate_content(
        self, prompt: str, audio_file: AudioFile, **kwargs: Any
    ) -> AsyncIterator[AIResponse]:
        """Streams the response chunk by chunk."""

        # Upload the audio file
        audio = await self.client.aio.files.upload(file=audio_file.file_path)

        async for chunk in await self.client.aio.models.generate_content_stream(
            model=self.model, contents=[prompt, audio], **kwargs
        ):
            if chunk.text:  # Only yield if there's actual content
                yield AIResponse(
                    content=chunk.text,
                    provider=Provider.GOOGLE,
                    metadata={"model": self.model, "is_stream_chunk": True},
                )

        # suppress final usage-only emission
