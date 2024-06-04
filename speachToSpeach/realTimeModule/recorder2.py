import sounddevice as sd
import numpy as np

class AudioRecorder:
    def __init__(self, fs: int = 44100, channels: int = 2, dtype: type = np.int16, silence_threshold: float = 1.0, silence_duration: float = 2.0) -> None:
        self.fs = fs
        self.channels = channels
        self.dtype = dtype
        self.recordings = []
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.silence_buffer = int(silence_duration * fs)
        self.silence_count = 0
        self.recording_active = False

    def callback(self, indata: np.ndarray, frames: int, time, status: dict) -> None:
        if status:
            print(status)
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

    def start(self) -> None:
        """Starts the audio recording."""
        try:
            self.stream = sd.InputStream(samplerate=self.fs, channels=self.channels, dtype=self.dtype, callback=self.callback)
            self.stream.start()
        except Exception as e:
            print(f"An error occurred while starting the recording: {e}")

    def get_audio_chunk(self, chunk_duration=10):
        if self.recordings:
            audio = np.concatenate(self.recordings, axis=0)
            chunk_size = self.fs * chunk_duration
            if len(audio) >= chunk_size:
                chunk = audio[:chunk_size]  # Get the first chunk_duration seconds of audio
                self.recordings = [audio[chunk_size:]]  # Keep the rest
                return chunk
        return None

    def stop(self) -> None:
        """Stops the audio recording."""
        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception as e:
                print(f"An error occurred while stopping the recording: {e}")
            finally:
                self.stream = None
