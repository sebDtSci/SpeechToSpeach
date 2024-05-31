import numpy as np
from faster_whisper import WhisperModel

from modules.gpuConfig import gpu_detection
import logging

class SpeachToText:
    def __init__(self, modelSize: str) -> None:
        self.modelSize = modelSize
        self.device = gpu_detection()
        self.model = self._initModel()

    def _initModel(self) -> WhisperModel:
        logging.info(f'device: {self.device}')
        return WhisperModel(self.modelSize, device=self.device, compute_type="int8")

    def transcribe(self, audio_segment: np.ndarray) -> None:
        segments, info = self.model.transcribe(audio_segment)
        text = "".join([segment.text for segment in segments])
        print(text)