import sounddevice as sd
import wavio
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
        # Calcule la norme du vecteur audio et on la divise par la racine carrée du nombre d'éléments pour normaliser
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
        """
        Starts the audio recording.

        Returns:
            None
        """
        self.stream = sd.InputStream(samplerate=self.fs, channels=self.channels, dtype=self.dtype, callback=self.callback)
        self.stream.start()

    def get_audio_chunk(self):
        if self.recordings:
            audio = np.concatenate(self.recordings, axis=0)
            return audio

    def stop(self) -> None:
        """
        Stops the audio recording.

        Returns:
            None
        """
        self.stream.stop()
        self.stream.close()
        self.stream = None


# import sounddevice as sd
# import wavio
# import numpy as np

# recordings = []

# class AudioRecorder:

#     def __init__(self, fs: int = 44100, channels: int = 2, dtype: type = np.int16, silence_threshold: float = 1.0, silence_duration: float = 2.0) -> None:
#         self.fs = fs
#         self.channels = channels
#         self.dtype = dtype
#         self.recordings = recordings
#         self.silence_threshold = silence_threshold
#         self.silence_duration = silence_duration
#         self.silence_buffer = int(silence_duration * fs)
#         self.silence_count = 0
#         self.recording_active = False

#     def callback(self, indata: np.ndarray, frames: int, time, status: dict) -> None:
        
#         # FIXME: fix this methode to interrupt the recording when the user stops speaking
#         if status:
#             print(status)
#         # NOTE: calcule la norme du vecteur audio et on la divise par la racine carré du nombre d'élément pour normaliser
#         volume = np.linalg.norm(indata) / np.sqrt(len(indata))
#         if volume < self.silence_threshold:
#             self.silence_count += frames
#         else:
#             self.silence_count = 0

#         if self.silence_count > self.silence_buffer:
#             self.recording_active = False
#         else:
#             self.recording_active = True
        
#         if self.recording_active:
#             self.recordings.append(indata.copy())
#         else:
#             self.stop()
            
#     def start(self) -> None:
#         """
#         Starts the audio recording.

#         Returns:
#             None
#         """
#         self.stream = sd.InputStream(samplerate=self.fs, channels=self.channels, dtype=self.dtype, callback=self.callback)
#         self.stream.start()

#     def get_audio_chunk(self):
#         if self.recordings:
#             audio = np.concatenate(self.recordings, axis=0)
#             return audio

#     def stop(self) -> None:
#         """
#         Stops the audio recording.

#         Returns:
#             None
#         """
#         self.stream.stop()
#         self.stream.close()
#         self.stream = None