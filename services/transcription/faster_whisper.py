import os
from services.transcription.base import TranscriptionProvider
from faster_whisper import WhisperModel
import logging

class FasterWhisperProvider(TranscriptionProvider):
    def __init__(self):
        # Configure model settings based on environment
        model_size = os.environ.get("WHISPER_MODEL", "small")
        device = os.environ.get("WHISPER_DEVICE", "cpu")
        compute_type = os.environ.get("WHISPER_COMPUTE_TYPE", "int8")
        
        logging.info(f"Loading faster-whisper model '{model_size}' on {device} with {compute_type}...")
        try:
            self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        except Exception as e:
            logging.error(f"Failed to load WhisperModel: {e}")
            raise RuntimeError(f"WhisperModel loading failed: {e}")

    def transcribe(self, audio_path: str) -> str:
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
        logging.info(f"Transcribing audio file: {audio_path}")
        # Transcribe without forcing translation to preserve Hindi/Hinglish
        segments, info = self.model.transcribe(audio_path, beam_size=5)
        
        logging.info(f"Detected language '{info.language}' with probability {info.language_probability}")
        
        transcript = ""
        for segment in segments:
            transcript += segment.text + " "
            
        return transcript.strip()
