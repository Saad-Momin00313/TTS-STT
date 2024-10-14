import json
import threading
import asyncio
from websockets.sync.client import connect
from config import Config
from audio_utils import save_to_wav

class TTSClient:
    def __init__(self, speaker):
        self._socket = connect(
            Config.DEEPGRAM_URL,
            additional_headers={"Authorization": f"Token {Config.DEEPGRAM_API_KEY}"}
        )
        self._exit = threading.Event()
        self._speaker = speaker
        self._receiver_thread = threading.Thread(target=asyncio.run, args=(self._receiver(),))
        self._receiver_thread.start()

    async def _receiver(self):
        audio_data = []
        try:
            while not self._exit.is_set():
                message = self._socket.recv()
                if message is None:
                    continue
                if isinstance(message, str):
                    print(message)
                elif isinstance(message, bytes):
                    self._speaker.play(message)
                    audio_data.append(message)
        except Exception as e:
            print(f"TTSClient._receiver error: {e}")
        finally:
            self._speaker.stop()
            save_to_wav(audio_data)

    def speak(self, text):
        self._socket.send(json.dumps({"type": "Speak", "text": text}))

    def flush(self):
        self._socket.send(json.dumps({"type": "Flush"}))

    def close(self):
        self._exit.set()
        self._socket.send(json.dumps({"type": "Close"}))
        self._socket.close()
        self._receiver_thread.join()