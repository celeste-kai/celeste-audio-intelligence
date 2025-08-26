from celeste_core.enums.capability import Capability
from celeste_core.enums.providers import Provider

# Capability for this domain package
CAPABILITY: Capability = Capability.AUDIO_TRANSCRIPTION

# Provider wiring for audio intelligence clients
PROVIDER_MAPPING: dict[Provider, tuple[str, str]] = {
    Provider.GOOGLE: (".providers.google", "GoogleAudioClient"),
    Provider.OPENAI: (".providers.openai", "OpenAIAudioClient"),
}

__all__ = ["CAPABILITY", "PROVIDER_MAPPING"]
