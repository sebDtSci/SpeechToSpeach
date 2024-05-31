from faster_whisper import WhisperModel
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()

AUDIOPATH = os.getenv("AUDIOPATH", "./")

class SpeachToText:

    def __init__(self, modelSize:str, inputAudio:np.ndarray) -> None:
        self.modelSize = modelSize
        self.inputAudio = inputAudio
        self.model = self._initModel()
    
    def _initModel(self) -> None:
        # TODO: Add GPU de tection for faster inference (Cuda, metal) -> create a new function to this specific task -> https://github.com/SYSTRAN/faster-whisper
        return WhisperModel(self.modelSize, device="cpu", compute_type="int8")
        
    def transcribe(self) -> str:
        segments, info = self.model.transcribe(self.inputAudio)
        return [segment.text for segment in segments] 

if __name__ == "__main__":
    stp = SpeachToText("medium", f"{AUDIOPATH}enregistrement_continue.wav")
    print(stp.transcribe())