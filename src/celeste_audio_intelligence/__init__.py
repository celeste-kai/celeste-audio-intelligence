"""
Celeste Audio Intelligence Client.
"""

from typing import Any

from celeste_core import Provider
from celeste_core.base.audio_client import BaseAudioClient
from celeste_core.config.settings import settings

from .mapping import PROVIDER_MAPPING

__version__ = "0.1.0"


def create_audio_client(provider: str | Provider, **kwargs: Any) -> BaseAudioClient:
    """
    Factory function to create an audio client instance based on the provider.

    Args:
        provider: The audio client provider to use (string or Provider enum).
        **kwargs: Additional arguments to pass to the audio client constructor.

    Returns:
        An instance of an audio client
    """
    # Normalize to enum
    provider_enum: Provider = (
        provider if isinstance(provider, Provider) else Provider(provider)
    )

    if provider_enum not in PROVIDER_MAPPING:
        raise ValueError(f"Unsupported provider: {provider_enum}")

    # Validate environment for the chosen provider
    settings.validate_for_provider(provider_enum.value)

    module_path, class_name = PROVIDER_MAPPING[provider_enum]
    module = __import__(
        f"celeste_audio_intelligence{module_path}", fromlist=[class_name]
    )
    audio_class = getattr(module, class_name)
    return audio_class(**kwargs)


__all__ = [
    "create_audio_client",
    "BaseAudioClient",
    "Provider",
    "__version__",
]
