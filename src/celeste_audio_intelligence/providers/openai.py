from typing import Any, AsyncIterator, Optional

import openai

from src.celeste_audio_intelligence import BaseAudioClient
from src.celeste_audio_intelligence.core.config import OPENAI_API_KEY
from src.celeste_audio_intelligence.core.enums import (
    AudioIntelligenceProvider,
    OpenAIAudioModel,
)
from src.celeste_audio_intelligence.core.types import AIResponse, AIUsage, AudioFile


class OpenAIAudioClient(BaseAudioClient):
    """OpenAI Audio Client for transcription using Whisper and GPT-4o models."""

    def __init__(
        self, model: str = OpenAIAudioModel.WHISPER.value, **kwargs: Any
    ) -> None:
        self.client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
        self.model_name = model

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

        # Whisper doesn't provide usage metadata
        usage = self.format_usage(None)

        # Return AIResponse object
        return AIResponse(
            content=response.text,
            usage=usage,
            provider=AudioIntelligenceProvider.OPENAI,
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

    def format_usage(self, usage_data: Any) -> Optional[AIUsage]:
        """OpenAI transcription APIs don't provide token usage information."""
        return AIUsage(
            input_tokens=0,
            output_tokens=0,
            total_tokens=0,
        )
