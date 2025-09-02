# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Celeste Audio Intelligence is a specialized package within the Celeste ecosystem focused on audio processing and transcription. It provides a unified interface for audio AI capabilities across multiple providers (Google, OpenAI) with support for various audio formats.

## Architecture

### Core Components
- **Factory Pattern**: `create_audio_client()` function creates provider-specific clients
- **Provider Mapping**: `mapping.py` maps Provider enums to implementation classes
- **Base Classes**: Inherits from `BaseAudioClient` in celeste-core
- **Type System**: Uses Pydantic models and custom enums for validation

### Directory Structure
```
src/celeste_audio_intelligence/
├── __init__.py                 # Main factory function
├── mapping.py                  # Provider-to-class mapping
├── core/
│   ├── enums.py               # AudioMimeType, model enums
│   └── types.py               # AudioFile type definitions
└── providers/
    ├── google.py              # Google Gemini implementation
    └── openai.py              # OpenAI Whisper implementation
```

## Development Commands

### Setup and Dependencies
```bash
uv sync                        # Install dependencies (preferred over pip)
```

### Running Examples
```bash
python example.py              # Streamlit demo app
streamlit run example.py       # Alternative way to run demo
```

### Code Quality
```bash
ruff check .                   # Linting
ruff format .                  # Code formatting
pre-commit run --all-files     # Run pre-commit hooks
```

## Key Patterns

### Provider Implementation
- Each provider inherits from `BaseAudioClient`
- Implements `generate_content(prompt, audio_file)` method
- Uses provider-specific API keys from environment variables
- Maps to Provider enum in `mapping.py`

### Audio File Handling
- Uses `AudioFile` type with `file_path` and `mime_type` parameters
- Supports multiple formats: MP3, WAV, FLAC, AAC, OGG, AIFF
- Handles both file paths and raw bytes

### Environment Configuration
- Requires provider API keys (GOOGLE_API_KEY, OPENAI_API_KEY)
- Settings validation through celeste-core
- No .env files in repository (created by users)

## Dependencies

### Core Dependencies
- `celeste-core>=0.1.0` - Base classes and shared functionality
- `pydantic>=2.11.7` - Data validation and serialization
- `google-genai>=0.1.0` - Google Gemini integration
- `openai>=1.91.0` - OpenAI API integration

### Development Dependencies
- `ruff>=0.12.1` - Linting and formatting
- `pre-commit>=4.2.0` - Git hooks
- `streamlit>=1.46.1` - Demo application

## Supported Models

### Google (Implemented)
- gemini-2.5-flash-lite-preview-06-17
- gemini-2.5-flash
- gemini-2.5-pro

### OpenAI (Implemented)
- whisper-1
- gpt-4o-transcribe
- gpt-4o-mini-transcribe

## Testing and Validation
- Uses capability-based validation from celeste-core
- Audio files in `data/` directory for testing
- Example usage in `example.py` demonstrates all functionality