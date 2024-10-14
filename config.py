import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')
    DEEPGRAM_URL = f"wss://api.deepgram.com/v1/speak?model=aura-helios-en&encoding=linear16&sample_rate=48000"
    AUDIO_FORMAT = 'int16'
    CHANNELS = 1
    RATE = 48000
    CHUNK = 4096
    TIMEOUT = 0.050