import os
from faster_whisper import WhisperModel

class SpeechToText:

    def __init__(self, model_path, input_audio_path):
        self.model = WhisperModel(model_path)
        self.input_audio = input_audio_path

    def transcribe(self):
        if not os.path.isfile(self.input_audio):
            raise FileNotFoundError(f"The file {self.input_audio} does not exist or is not readable.")
        with open(self.input_audio, 'rb') as f:
            audio_data = f.read()
        segments, info = self.model.transcribe(self.input_audio)
        return segments, info