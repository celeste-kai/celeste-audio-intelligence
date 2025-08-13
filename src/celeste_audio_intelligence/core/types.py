from pathlib import Path
from typing import Optional

from celeste_core import AIResponse
from pydantic import BaseModel, ConfigDict


class AudioFile(BaseModel):
    """Represents an audio file with metadata."""

    model_config = ConfigDict(frozen=True)

    file_path: Path
    mime_type: str
    duration: Optional[float] = None
    sample_rate: Optional[int] = None
    channels: Optional[int] = None


__all__ = ["AudioFile", "AIResponse"]
