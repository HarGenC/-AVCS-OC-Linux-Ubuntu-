import json, pyaudio
from vosk import Model, KaldiRecognizer
from threading import Thread
from LoadSettings import *
import time


class SpeechConversion():
    def __init__(self, func, parent=None):
        self.func = func
        self.loadSettings()
        self.Run = True
        th = Thread(target = self.listen)
        th.start()

    def loadSettings(self):
        self.model = Model('small_model')
        self.rec = KaldiRecognizer(self.model, 16000)
        self.p = pyaudio.PyAudio()
        self.MicrophoneID = self.getMicrophoneID()

    def listen(self):
        stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000, input_device_index=self.MicrophoneID)
        stream.start_stream()
        while self.Run:
        	data = stream.read(4000, exception_on_overflow=False)
        	if (self.rec.AcceptWaveform(data)) and (len(data) > 0):
        		answer = json.loads(self.rec.Result())
        		#if answer['text']:
        			#self.func(answer['text'])
        	else:
        		result = json.loads(self.rec.PartialResult())
        		#if result['partial']:
        		self.func(result['partial'])
        stream.stop_stream()

    def stop(self):
        self.Run = False

    def changeMicrophone(self):
        self.Run = False
        time.sleep(0.5)
        self.MicrophoneID = self.getMicrophoneID()
        self.Run = True
        th = Thread(target = self.listen)
        th.start()

    def getMicrophoneID(self):
        ls = LoadSettings()
        Microphone = ls.LoadSettings()["MicrophoneName"]
        MicrophoneList = []
        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            if (self.p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                if self.p.get_device_info_by_host_api_device_index(0, i).get('name') == Microphone:
                    return i
        return 0