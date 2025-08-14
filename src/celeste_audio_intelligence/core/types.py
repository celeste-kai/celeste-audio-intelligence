from pathlib import Path
from typing import Optional

from celeste_core import AIResponse
from pydantic import BaseModel, ConfigDict


class AudioFile(BaseModel):
    """Represents an audio file with metadata."""

    model_config = ConfigDict(frozen=True)

    file_path: Optional[Path] = None
    data: Optional[bytes] = None
    filename: Optional[str] = None  # For APIs that need a filename
    mime_type: str = "audio/mpeg"
    duration: Optional[float] = None
    sample_rate: Optional[int] = None
    channels: Optional[int] = None


__all__ = ["AudioFile", "AIResponse"]
