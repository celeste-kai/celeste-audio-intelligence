from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict

from src.celeste_audio_intelligence.core.enums import AudioIntelligenceProvider


class AudioFile(BaseModel):
    """Represents an audio file with metadata."""

    model_config = ConfigDict(frozen=True)

    file_path: Path  # Path to the audio file
    mime_type: str  # MIME type of the audio file (e.g., "audio/mpeg", "audio/wav")
    duration: Optional[float] = None  # Duration of the audio in seconds, if known
    sample_rate: Optional[int] = None  # Sample rate of the audio, if known
    channels: Optional[int] = None  # Number of audio channels, if known


class AIUsage(BaseModel):
    """Token usage metrics for AI responses."""

    model_config = ConfigDict(frozen=True)

    input_tokens: int
    output_tokens: int
    total_tokens: int


class AIResponse(BaseModel):
    """Response from AI providers."""

    model_config = ConfigDict(frozen=True)

    content: str
    usage: Optional[AIUsage] = None
    provider: Optional[AudioIntelligenceProvider] = None
    metadata: Dict[str, Any] = {}
