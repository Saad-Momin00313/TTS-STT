from speaker import Speaker
from tts_client import TTSClient
from chatbot import Chatbot
from audio_utils import list_audio_devices

def main():
    print("Available audio output devices:")
    devices = list_audio_devices()
    for id, name in devices:
        print(f"Output Device id {id} - {name}")

    device_id = int(input("Enter the desired output device ID (or press Enter for default): ") or "-1")
    chatbot_name = input("Enter a name for your chatbot: ")

    speaker = Speaker(output_device_index=device_id if device_id >= 0 else None)
    speaker.start()
    tts_client = TTSClient(speaker)
    chatbot = Chatbot(chatbot_name, tts_client)
    chatbot.start_conversation()

    tts_client.close()
    speaker.stop()

if __name__ == "__main__":
    main()
