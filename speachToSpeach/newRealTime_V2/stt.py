import pyaudio
import numpy as np
from faster_whisper import WhisperModel
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Configuration de l'enregistrement audio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

model = WhisperModel("base")

print("Transcription en temps réel...")

try:
    while True:
        frames = [stream.read(CHUNK) for _ in range(5)]
        audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
        
        # Transcrire l'audio
        segments, info = model.transcribe(audio_data)

        for segment in segments:
            print(f"Début: {segment['start']} - Fin: {segment['end']} - Texte: {segment['text']}")
except KeyboardInterrupt:
    print("Transcription terminée")

# Arrêt du flux et fermeture
stream.stop_stream()
stream.close()
audio.terminate()