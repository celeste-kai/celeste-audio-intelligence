import io
from collections.abc import AsyncIterator
from typing import Any

from pydantic import BaseModel

from celeste_core import AIResponse, AudioArtifact, Provider
from celeste_core.base.audio_client import BaseAudioClient
from celeste_core.config.settings import settings
from celeste_core.enums.capability import Capability
from google import genai


class GoogleAudioClient(BaseAudioClient):
    def __init__(self, model: str = "gemini-2.5-flash", **kwargs: Any) -> None:
        super().__init__(
            model=model,
            capability=Capability.AUDIO_TRANSCRIPTION,
            provider=Provider.GOOGLE,
            **kwargs,
        )
        self.client = genai.Client(api_key=settings.google.api_key)

    async def generate_content(
        self,
        prompt: str,
        audio_file: AudioArtifact,
        structured_output: BaseModel | list[BaseModel] | None = None,
        **kwargs: Any,
    ) -> AIResponse:
        """Generate text from a prompt and a list of documents."""
        audio = await self._upload_audio(audio_file)

        request_kwargs = self._prepare_request_config(structured_output, kwargs)

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=[prompt, audio],
            **request_kwargs,
        )

        # Return AIResponse object
        return AIResponse(
            content=getattr(response, "parsed", response.text),
            provider=Provider.GOOGLE,
            metadata={"model": self.model},
        )

    async def stream_generate_content(
        self,
        prompt: str,
        audio_file: AudioArtifact,
        structured_output: BaseModel | list[BaseModel] | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[AIResponse]:
        """Streams the response chunk by chunk."""

        audio = await self._upload_audio(audio_file)

        request_kwargs = self._prepare_request_config(structured_output, kwargs)

        async for chunk in await self.client.aio.models.generate_content_stream(
            model=self.model, contents=[prompt, audio], **request_kwargs
        ):
            parsed_content = getattr(chunk, "parsed", None)
            text_content = getattr(chunk, "text", None)

            if parsed_content is None and not text_content:
                continue

            yield AIResponse(
                content=parsed_content if parsed_content is not None else text_content,
                provider=Provider.GOOGLE,
                metadata={"model": self.model, "is_stream_chunk": True},
            )

        # suppress final usage-only emission

    async def _upload_audio(self, audio_file: AudioArtifact) -> Any:
        """Upload audio file from bytes or path."""

        if audio_file.data:
            audio_buffer = io.BytesIO(audio_file.data)
            audio_buffer.name = "audio.mp3"
            return await self.client.aio.files.upload(file=audio_buffer)

        if audio_file.path:
            return await self.client.aio.files.upload(file=audio_file.path)

        raise ValueError("AudioArtifact must have either data or path")

    def _prepare_request_config(
        self,
        structured_output: BaseModel | list[BaseModel] | None,
        kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        """Prepare request kwargs including structured output configuration."""

        request_kwargs = dict(kwargs)

        if structured_output is not None:
            request_kwargs["config"] = {
                "response_mime_type": "application/json",
                "response_schema": structured_output,
            }

        return request_kwargs
