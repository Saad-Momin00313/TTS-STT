import pyaudio
import queue
import threading
from config import Config

class Speaker:
    def __init__(self, rate=Config.RATE, chunk=Config.CHUNK, channels=Config.CHANNELS, output_device_index=None):
        self._exit = threading.Event()
        self._queue = queue.Queue()
        self._audio = pyaudio.PyAudio()
        self._chunk = chunk
        self._rate = rate
        self._format = getattr(pyaudio, f'pa{Config.AUDIO_FORMAT.capitalize()}')
        self._channels = channels
        self._output_device_index = output_device_index
        self._buffer = b''
        self._stream = None
        self._thread = None

    def start(self):
        self._stream = self._audio.open(
            format=self._format,
            channels=self._channels,
            rate=self._rate,
            input=False,
            output=True,
            frames_per_buffer=self._chunk,
            output_device_index=self._output_device_index,
        )
        self._exit.clear()
        self._thread = threading.Thread(target=self._play, daemon=True)
        self._thread.start()
        self._stream.start_stream()
        return True

    def stop(self):
        self._exit.set()
        if self._stream is not None:
            self._stream.stop_stream()
            self._stream.close()
            self._stream = None
        if self._thread is not None:
            self._thread.join()
            self._thread = None
        self._queue = queue.Queue()

    def play(self, data):
        self._queue.put(data)

    def _play(self):
        while not self._exit.is_set():
            try:
                data = self._queue.get(timeout=Config.TIMEOUT)
                self._buffer += data
                while len(self._buffer) >= self._chunk:
                    chunk = self._buffer[:self._chunk]
                    self._buffer = self._buffer[self._chunk:]
                    self._stream.write(chunk)
            except queue.Empty:
                if self._buffer:
                    self._stream.write(self._buffer)
                    self._buffer = b''
            except Exception as e:
                print(f"Speaker._play error: {e}")