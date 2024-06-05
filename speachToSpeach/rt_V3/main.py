from recorder import SoundReceiverModule
# from stt import SpeechToText
import time
import os

AUDIOPATH = os.getenv("AUDIOPATH", "./")
TEXTPATH = os.getenv("TEXTPATH", "./")
output_audio_file = os.path.join(AUDIOPATH, "enregistrement_continue.wav")
output_text = os.path.join(TEXTPATH, "enregistrement_continue.raw")

recorder = SoundReceiverModule(output_wav_file=output_audio_file, output_speech_detected_file=output_text,channel=0,seconds_to_keep=15,\
                        sample_rate=45000,loudness_threshold=0.63)
recorder.start()
# print("Press 's' to stop recording...")