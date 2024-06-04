import time
import numpy as np
from recorder2 import AudioRecorder
from tts import SpeachToText
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

def main():
    audio_recorder = AudioRecorder()
    speech_to_text = SpeachToText("medium")
    audio_recorder.start()
    print("Start speaking...")

    try:
        while True:
            audio_chunk = audio_recorder.get_audio_chunk(chunk_duration=5)  # 5 seconds chunks
            if audio_chunk is not None and len(audio_chunk) > 0:
                speech_to_text.transcribe(audio_chunk)
            time.sleep(0.1)  # Adjust for desired latency
    except KeyboardInterrupt:
        audio_recorder.stop()
        print("Stopped recording.")
    except Exception as e:
        audio_recorder.stop()
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()