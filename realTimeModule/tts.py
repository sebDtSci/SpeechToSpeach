import numpy as np
from faster_whisper import WhisperModel

class SpeachToText:
    def __init__(self, modelSize: str) -> None:
        self.modelSize = modelSize
        self.model = self._initModel()

    def _initModel(self) -> WhisperModel:
        return WhisperModel(self.modelSize, device="cpu", compute_type="int8")

    def transcribe(self, audio_segment: np.ndarray) -> None:
        segments, info = self.model.transcribe(audio_segment)
        text = "".join([segment.text for segment in segments])
        print(text)
        # for segment in segments:
        #     print(segment.text)