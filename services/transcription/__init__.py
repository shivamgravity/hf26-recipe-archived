import os
from services.transcription.base import TranscriptionProvider

def get_transcription_provider() -> TranscriptionProvider:
    provider = os.environ.get("TRANSCRIPTION_PROVIDER", "local").lower()
    
    if provider == "local":
        try:
            from services.transcription.faster_whisper import FasterWhisperProvider
            return FasterWhisperProvider()
        except ImportError as e:
            import logging
            logging.error(f"Could not load faster-whisper ({e}). Falling back to mock.")
            from services.transcription.mock import MockWhisperProvider
            return MockWhisperProvider()
    else:
        from services.transcription.mock import MockWhisperProvider
        return MockWhisperProvider()
