import numpy as np
from faster_whisper import WhisperModel
import sys
sys.path.append('../')

from SpeachToSpeach.speachToSpeach.modules.gpuConfig import gpu_detection
import logging

class SpeachToText:
    def __init__(self, modelSize: str) -> None:
        self.modelSize = modelSize
        self.device = gpu_detection()
        self.model = self._initModel()
        self._stopWords = [" Thanks for watching!"]

    def _blankTest(self, text: str) -> bool:
        return text in self._stopWords

    def _initModel(self) -> WhisperModel:
        logging.info(f'device: {self.device}')
        try:
            return WhisperModel(self.modelSize, device=self.device, compute_type="int8")
        except Exception as e:
            logging.error(f"Failed to initialize the model: {e}")
            raise

    def transcribe(self, audio_segment: np.ndarray) -> None:
        try:
            segments, info = self.model.transcribe(audio_segment)
            text = "".join([segment.text for segment in segments])
            if not self._blankTest(text):
                print(text)
        except Exception as e:
            logging.error(f"Transcription failed: {e}")



# import numpy as np
# from faster_whisper import WhisperModel
# import sys
# sys.path.append('../')

# from SpeachToSpeach.speachToSpeach.modules.gpuConfig import gpu_detection
# import logging

# class SpeachToText:
#     def __init__(self, modelSize: str) -> None:
#         self.modelSize = modelSize
#         self.device = gpu_detection()
#         self.model = self._initModel()
#         self._stopWords:list[str] = [" Thanks for watching!"]

#     def _blankTest(self, text:str) -> bool:
#         if text in self._stopWords:
#             return True
#         else:
#             return False

#     def _initModel(self) -> WhisperModel:
#         logging.info(f'device: {self.device}')
#         return WhisperModel(self.modelSize, device=self.device, compute_type="int8")

#     def transcribe(self, audio_segment: np.ndarray) -> None:
#         segments, info = self.model.transcribe(audio_segment)
#         text = "".join([segment.text for segment in segments])
#         if not self._blankTest(text):
#             print(text)