import sounddevice as sd
import wavio
import numpy as np
import keyboard
from dotenv import load_dotenv
import os

load_dotenv()
AUDIOPATH = os.getenv("AUDIOPATH", "./")
print(f"AUDIOPATH : {AUDIOPATH}")
recordings = []

class AudioRecorder:

    def __init__(self, fs: int = 44100, channels: int = 1, dtype: type = np.int16, silence_threshold: float = 1.0, silence_duration: float = 2.0) -> None:
        self.fs = fs
        self.channels = channels
        self.dtype = dtype
        self.recordings = recordings
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.silence_buffer = int(silence_duration * fs)
        self.silence_count = 0
        self.recording_active = False
        self.stream = None

    def callback(self, indata: np.ndarray, frames: int, time, status: dict) -> None:
        if status:
            print('status:', status)
        volume = np.linalg.norm(indata) / np.sqrt(len(indata))
        if volume < self.silence_threshold:
            self.silence_count += frames
        else:
            self.silence_count = 0

        if self.silence_count > self.silence_buffer:
            self.recording_active = False
        else:
            self.recording_active = True

        if self.recording_active:
            self.recordings.append(indata.copy())
        else:
            self.stop()
            
    def start(self) -> None:
        try:
            self.stream = sd.InputStream(samplerate=self.fs, channels=self.channels, dtype=self.dtype, callback=self.callback)
            self.stream.start()
        except sd.PortAudioError as e:
            print(f"PortAudioError: {e}")
            print("Unable to open input stream with 1 channel.")

    def stop(self) -> None:
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

    def get_audio_chunk(self, chunk_duration=10):
        if self.recording_active:
            audio = np.concatenate(self.recordings, axis=0)
            chunk_size = self.fs * chunk_duration
            if len(audio) >= chunk_size:
                chunk = audio[:chunk_size]
                self.recordings = [audio[chunk_size:]]
                return chunk
        return None

    def write(self) -> None:
        if self.recording_active:
            audio = np.concatenate(self.recordings, axis=0)
            output_path = os.path.join(AUDIOPATH, "enregistrement_continue.wav")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            wavio.write(output_path, audio, self.fs, sampwidth=2)
        else:
            print("Aucune donnée enregistrée.")