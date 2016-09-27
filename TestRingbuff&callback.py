import numpy as np
from sys import byteorder
from array import array
from struct import pack
from time import process_time
import datetime

import pyaudio
import wave
import timeit


class RingBuffer():
    "A 1D ring buffer using numpy arrays"
    def __init__(self, length):
        self.data = np.zeros(length, dtype='f')
        self.index = 0

    def extend(self, x):
        "adds array x to ring buffer"
        x_index = (self.index + np.arange(x.size)) % self.data.size
        self.data[x_index] = x
        self.index = x_index[-1] + 1

    def get(self):
        "Returns the first-in-first-out data in the ring buffer"
        idx = (self.index + np.arange(self.data.size)) %self.data.size
        return self.data[idx]

def ringbuff_numpy_test():
    ringlen = 100000
    ringbuff = RingBuffer(ringlen)
    for i in range(40):
        ringbuff.extend(np.zeros(10000, dtype='f')) # write
        ringbuff.get() #read


# Autorecording choices, seconds
THRESHOLD = 7000
TimeBeforeStart = 3
TimeAfterEnd = 3
AudioSaveToPath = "slask\\"

# pyaudio settings
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
# FORMAT = np.int16
MAXIMUM = 16384
RATE = 44100
ARRAYTYPE = array('h') 

def AnalyzeChunk(snd_data): # former is_silent
    "Returns 'True' if below the 'silent' threshold"
    #print(max(snd_data), end=", ", flush=True)

    return max(snd_data) # < THRESHOLD


def listen() :
     # Startar pyAudio
    p = pyaudio.PyAudio()
    # Öppnar en p.stream
    stream = p.open(format = FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)
    
    ChunkQ = array('h')
    ListQ  = [[("points", "max",  "silent","chunk")]]
    TimeList = [["ii", "Anatime","Arrtime", "Listtime"]]

    for ii in range(100) :
        snd_data = array('h', stream.read(CHUNK_SIZE))
        # arr = np.aray(snd_data)
        repetitions = range(1000)    
        if byteorder == 'big':
            snd_data.byteswap()

        # Är chunken tyst??
        # Anatime0 = process_time()
        # for xx in  range(2000) :
        ChunkMaxAmp = AnalyzeChunk(snd_data)
        # Anatime = process_time() - Anatime0

        if ChunkMaxAmp < THRESHOLD :
            silent = True
        else :
            silent = False

        # Addera t kön
        # Arrtime0 = process_time()
        # for xx in  range(2000)  :
        ChunkQ.extend(snd_data)
        # Arrtime = -(Arrtime0 - process_time())
        # ListQ.append(ii,("prp",snd_data))
        # Listtime0 = process_time()
        # for xx in  range(2000)  :
        ListQ.append([("points",ChunkMaxAmp,silent,snd_data)])
        # Listtime = -(Listtime0 - process_time())

        # TimeList.append([(ii,Anatime, Arrtime,Listtime)])



    x=0


# ringbuff_numpy_test()

listen()