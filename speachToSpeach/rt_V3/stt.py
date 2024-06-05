import os
from faster_whisper import WhisperModel
import time
import logging
from dotenv import load_dotenv

class SpeechToText:

    def __init__(self, model_path:str="medium", input_audio_path:str=None, output_file:str=None):
        self.model = WhisperModel(model_path)
        self.input_audio = input_audio_path
        self.output_file = output_file
        self.transcribtion = ""
    
    def _write(self):
        with open(self.output_file, 'w') as f:
            f.write(self.transcribtion)

    def start(self):
        if not os.path.isfile(self.input_audio):
            raise FileNotFoundError(f"The file {self.input_audio} does not exist or is not readable.")
        
        self.running = True

        while self.running:
            try:
                segments, info = self.model.transcribe(self.input_audio)
                text = " ".join([segment.text for segment in segments])
                self.transcribtion = text
                self._write()
                time.sleep(0.1)
            except Exception as e:
                logging.error(f"Transcription failed: {e}")
    
if __name__ == "__main__":
    load_dotenv()

    AUDIOPATH = os.getenv("AUDIOPATHW", "./")
    TEXTPATH = os.getenv("TEXTPATHW", "./")
    output_audio_file = os.path.join(AUDIOPATH, "enregistrement_continue.wav")
    output_text = os.path.join(TEXTPATH, "sortie.txt")
    
    
    stt = SpeechToText("medium", output_audio_file, output_text)
    stt.start()
