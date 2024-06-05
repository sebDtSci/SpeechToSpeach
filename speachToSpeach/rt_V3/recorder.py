import sounddevice as sd
import numpy as np
import time
import logging
import wave
import os

class SoundReceiverModule:
    def __init__(self, output_wav_file, output_speech_detected_file, channel, seconds_to_keep, sample_rate, loudness_threshold):
        self.__wav_file = output_wav_file
        self.__raw_file = output_wav_file.replace(".wav", ".raw")
        self.__speech_detected_file = output_speech_detected_file
        self.__channel = channel
        self.__sample_rate = sample_rate
        self.__samples_to_keep = seconds_to_keep * sample_rate
        self.__loudness_threshold = loudness_threshold

        self.__running = False
        self.__aSoundData = None

        self.__rfile = None

    def __write_wav_to_file_from_raw(self):
        """write the wav file from the raw file"""
        with open(self.__raw_file, 'rb') as raw_file:
            raw_data = raw_file.read()

        raw_data = raw_data[-self.__samples_to_keep * 2:]  # keep only the last N seconds

        wav_file = wave.open(self.__wav_file, 'wb')
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(self.__sample_rate)
        wav_file.writeframes(raw_data)

        wav_file.close()

    def __write_time_speech_detected_to_file(self):
        """write the current time to the file"""
        with open(self.__speech_detected_file, 'w') as file:
            file.write("speech detected at: " + time.strftime("%c") + "\n")

    def __speechDetected(self):
        """return True if the given sound data is a speech"""
        n1 = self.__soundDataLoudness(self.__aSoundData)
        return n1 > self.__loudness_threshold

    def __soundDataLoudness(self, aSoundDataChannel):
        """compute the loudness of the given sound data, between 0 and 1"""
        return 1 - (np.sqrt(np.mean(1**2)) / 100)

    def get_running(self):
        return self.__running

    def get_channel(self):
        return self.__channel

    def set_channel(self, channel):
        self.__channel = channel

    def get_samples_to_keep(self):
        return self.__samples_to_keep

    def set_samples_to_keep(self, samples_to_keep):
        self.__samples_to_keep = samples_to_keep

    def get_loudness_threshold(self):
        return self.__loudness_threshold

    def set_loudness_threshold(self, loudness_threshold):
        self.__loudness_threshold = loudness_threshold

    def start(self):
        """launch the listening process (this is a non-blocking call)"""
        self.__rfile = open(self.__raw_file, 'wb')
        self.__running = True

        logging.info("Record: started!")
        print('recording ...')

        with sd.InputStream(callback=self.__processRemote, channels=1, samplerate=self.__sample_rate, dtype='int16'):
            while self.__running:
                sd.sleep(1000)  # keep the stream open

    def stop(self):
        """stop the listening process"""
        self.__running = False
        if self.__rfile:
            self.__rfile.close()
        logging.info("T6_RecordAudio: Finished.")

    def __processRemote(self, indata, frames, time, status):
        """This is the method that receives all the sound buffers from the sounddevice input stream"""
        if not self.__running:
            return

        self.__aSoundData = np.array(indata).flatten()
        self.__rfile.write(self.__aSoundData.tobytes())
        self.__write_wav_to_file_from_raw()

        if self.__speechDetected():
            self.__write_time_speech_detected_to_file()

# Example usage
if __name__ == "__main__":
    AUDIOPATH = os.getenv("AUDIOPATH", "./")
    TEXTPATH = os.getenv("TEXTPATH", "./")
    output_wav_file = os.path.join(AUDIOPATH, "enregistrement_continue.wav")
    output_speech_detected_file = os.path.join(TEXTPATH, "enregistrement_continue.raw")

    channel = 0
    seconds_to_keep = 10
    sample_rate = 16000
    loudness_threshold = 0.01

    sound_receiver = SoundReceiverModule(output_wav_file, output_speech_detected_file, channel, seconds_to_keep, sample_rate, loudness_threshold)
    try:
        sound_receiver.start()
    except KeyboardInterrupt:
        sound_receiver.stop()

# import sounddevice as sd
# import numpy as np
# import time
# import logging
# import wave
# import os

# class SoundReceiverModule:
#     def __init__(self, output_wav_file, output_speech_detected_file, channel, seconds_to_keep, sample_rate, loudness_threshold):
#         self.__wav_file = output_wav_file
#         self.__raw_file = output_wav_file.replace(".wav", ".raw")
#         self.__speech_detected_file = output_speech_detected_file
#         self.__channel = channel
#         self.__sample_rate = sample_rate
#         self.__samples_to_keep = seconds_to_keep * sample_rate
#         self.__loudness_threshold = loudness_threshold

#         self.__running = False
#         self.__aSoundData = None

#         self.__rfile = None

#     def __write_wav_to_file_from_raw(self):
#         """write the wav file from the raw file"""
#         with open(self.__raw_file, 'rb') as raw_file:
#             raw_data = raw_file.read()

#         raw_data = raw_data[-self.__samples_to_keep * 2:]  # keep only the last N seconds

#         wav_file = wave.open(self.__wav_file, 'wb')
#         wav_file.setnchannels(1)
#         wav_file.setsampwidth(2)
#         wav_file.setframerate(self.__sample_rate)
#         wav_file.writeframes(raw_data)

#         wav_file.close()

#     def __write_time_speech_detected_to_file(self):
#         """write the current time to the file"""
#         with open(self.__speech_detected_file, 'w') as file:
#             file.write("speech detected at: " + time.strftime("%c") + "\n")

#     def __speechDetected(self):
#         """return True if the given sound data is a speech"""
#         n1 = self.__soundDataLoudness(self.__aSoundData)
#         return n1 > self.__loudness_threshold

#     def __soundDataLoudness(self, aSoundDataChannel):
#         """compute the loudness of the given sound data, between 0 and 1"""
#         return 1 - (np.sqrt(np.mean(aSoundDataChannel**2)) / 100)

#     def get_running(self):
#         return self.__running

#     def get_channel(self):
#         return self.__channel

#     def set_channel(self, channel):
#         self.__channel = channel

#     def get_samples_to_keep(self):
#         return self.__samples_to_keep

#     def set_samples_to_keep(self, samples_to_keep):
#         self.__samples_to_keep = samples_to_keep

#     def get_loudness_threshold(self):
#         return self.__loudness_threshold

#     def set_loudness_threshold(self, loudness_threshold):
#         self.__loudness_threshold = loudness_threshold

#     def start(self):
#         """launch the listening process (this is a non-blocking call)"""
#         self.__rfile = open(self.__raw_file, 'wb')
#         self.__running = True

#         logging.info("RecordAudio: started!")

#         with sd.InputStream(callback=self.__processRemote, channels=1, samplerate=self.__sample_rate):
#             while self.__running:
#                 sd.sleep(1000)  # keep the stream open

#     def stop(self):
#         """stop the listening process"""
#         self.__running = False
#         if self.__rfile:
#             self.__rfile.close()
#         logging.info("T6_RecordAudio: Finished.")

#     def __processRemote(self, indata, frames, time, status):
#         """This is the method that receives all the sound buffers from the sounddevice input stream"""
#         if not self.__running:
#             return

#         self.__aSoundData = np.array(indata).flatten()
#         self.__rfile.write(self.__aSoundData.tobytes())
#         self.__write_wav_to_file_from_raw()

#         if self.__speechDetected():
#             self.__write_time_speech_detected_to_file()

# # Example usage
# if __name__ == "__main__":

#     AUDIOPATH = os.getenv("AUDIOPATH", "./")
#     TEXTPATH = os.getenv("TEXTPATH", "./")
#     output_audio_file = os.path.join(AUDIOPATH, "enregistrement_continue.wav")
#     output_text = os.path.join(TEXTPATH, "enregistrement_continue.raw")

#     channel = 0
#     seconds_to_keep = 5
#     sample_rate = 45000
#     loudness_threshold = 0.01

#     sound_receiver = SoundReceiverModule(output_audio_file, output_text, \
#                                         channel, seconds_to_keep, sample_rate, loudness_threshold)
#     try:
#         sound_receiver.start()
#     except KeyboardInterrupt:
#         sound_receiver.stop()