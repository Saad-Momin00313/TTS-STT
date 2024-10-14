import pyaudio
import wave
from config import Config

def list_audio_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    devices = []
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')) > 0:
            devices.append((i, p.get_device_info_by_host_api_device_index(0, i).get('name')))
    p.terminate()
    return devices

def save_to_wav(audio_data, filename="output.wav"):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(Config.CHANNELS)
    wf.setsampwidth(pyaudio.get_sample_size(getattr(pyaudio, f'paInt16')))
    wf.setframerate(Config.RATE)
    wf.writeframes(b''.join(audio_data))
    wf.close()
    print(f"Audio saved to {filename}")