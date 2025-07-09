from typing import Any, AsyncIterator, Optional

from celeste_client.core.enums import GeminiModel
from google import genai

from celeste_audio_intelligence import BaseAudioClient
from celeste_audio_intelligence.core.config import GOOGLE_API_KEY
from celeste_audio_intelligence.core.enums import AudioIntelligenceProvider
from celeste_audio_intelligence.core.types import AIResponse, AIUsage, AudioFile


class GoogleAudioClient(BaseAudioClient):
    def __init__(
        self, model: str = GeminiModel.FLASH_LITE.value, **kwargs: Any
    ) -> None:
        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        self.model_name = model

    async def generate_content(
        self, prompt: str, audio_file: AudioFile, **kwargs: Any
    ) -> AIResponse:
        """Generate text from a prompt and a list of documents."""

        audio = await self.client.aio.files.upload(file=audio_file.file_path)

        response = await self.client.aio.models.generate_content(
            model=self.model_name,
            contents=[prompt, audio],
        )

        # Convert usage data if available
        usage = self.format_usage(getattr(response, "usage_metadata", None))

        # Return AIResponse object
        return AIResponse(
            content=response.text,
            usage=usage,
            provider=AudioIntelligenceProvider.GOOGLE,
            metadata={"model": self.model_name},
        )

    async def stream_generate_content(
        self, prompt: str, audio_file: AudioFile, **kwargs: Any
    ) -> AsyncIterator[AIResponse]:
        """Streams the response chunk by chunk."""

        # Upload the audio file
        audio = await self.client.aio.files.upload(file=audio_file.file_path)

        last_usage_metadata = None
        async for chunk in await self.client.aio.models.generate_content_stream(
            model=self.model_name, contents=[prompt, audio]
        ):
            if chunk.text:  # Only yield if there's actual content
                yield AIResponse(
                    content=chunk.text,
                    provider=AudioIntelligenceProvider.GOOGLE,
                    metadata={"model": self.model_name, "is_stream_chunk": True},
                )
            if hasattr(chunk, "usage_metadata") and chunk.usage_metadata:
                last_usage_metadata = chunk.usage_metadata

        usage = self.format_usage(last_usage_metadata)
        if usage:
            yield AIResponse(
                content="",  # Empty content for the usage-only response
                usage=usage,
                provider=AudioIntelligenceProvider.GOOGLE,
                metadata={"model": self.model_name, "is_final_usage": True},
            )

    def format_usage(self, usage_data: Any) -> Optional[AIUsage]:
        """Convert Gemini usage data to AIUsage."""
        if not usage_data:
            return None
        return AIUsage(
            input_tokens=getattr(usage_data, "prompt_token_count", 0),
            output_tokens=getattr(usage_data, "candidates_token_count", 0),
            total_tokens=getattr(usage_data, "total_token_count", 0),
        )
