import time
import numpy as np
from recorder2 import AudioRecorder
from tts import SpeachToText

def main():
    audio_recorder = AudioRecorder()
    speech_to_text = SpeachToText("medium")
    audio_recorder.start()
    print("Start speaking...")

    try:
        while True:
            audio_chunk = audio_recorder.get_audio_chunk()
            speech_to_text.transcribe(audio_chunk)
            time.sleep(0.1)  # Ajuster pour la latence désirée
    except KeyboardInterrupt:
        audio_recorder.stop()
        print("Stopped recording.")

if __name__ == "__main__":
    main()