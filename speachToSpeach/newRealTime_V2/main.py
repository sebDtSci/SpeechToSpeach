import os
from recorder import AudioRecorder
from audioToText import SpeechToText
import time

AUDIOPATH = os.getenv("AUDIOPATH", "./")
# AUDIOPATH = '/Users/athena/Documents/projetGit/SpeachToSpeach/data/audio'
# AUDIOPATH = 'C:\\Users\\stadiello\\Documents\\projet\\SpeachToSpeach\\data\\audio\\'
output_audio_file = os.path.join(AUDIOPATH, "enregistrement_continue.wav")

recorder = AudioRecorder()
recorder.start()
print("Press 's' to stop recording...")
time.sleep(5)
if recorder.recording_active:
    recorder.stop()
recorder.write()

if os.path.exists(output_audio_file) and os.path.getsize(output_audio_file) > 0:
    speech_to_text = SpeechToText(model_path="medium", input_audio_path=output_audio_file)
    segments, info = speech_to_text.transcribe()

    print("Transcription:")
    for segment in segments:
        print(f"[{segment.start:.2f}s - {segment.end:.2f}s] {segment.text}")
else:
    print("The audio file was not created or is empty.")