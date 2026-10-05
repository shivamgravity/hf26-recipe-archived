import time
from services.transcription.base import TranscriptionProvider

class MockWhisperProvider(TranscriptionProvider):
    def transcribe(self, audio_path: str) -> str:
        # Simulate processing time
        time.sleep(1.5)
        # We return a dummy transcript for testing purposes
        return "Beta aaj aloo jeera banaya tha. Pehle chaar aloo ubaal lena. Phir kadhai mein do chamach tel garam karna hai. Usmein jeera daalna hai. Phir thodi si haldi aur namak apne hisaab se. Aloo daal ke achhe se bhunna hai jab tak thode crispy ho jaayein. Zyada paani mat daalna, warna maza nahi aayega."
