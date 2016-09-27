import numpy as np
from sys import byteorder
from array import array
from struct import pack
from time import process_time
import datetime
import matplotlib.pyplot as plt

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



def listen() :
     # Startar pyAudio
    p = pyaudio.PyAudio()
    # Öppnar en p.stream
    stream = p.open(format = FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)
    
    ListQ  = [[("silent", "Max", "Std", "MeaDivMed", "points", "arg", "Var", "Mean", "Median"),[]]]
    TimeList = [["ii", "Anatime","Arrtime", "Listtime"]]

    for ii in range(100) :
        #snd_data = array('h', stream.read(CHUNK_SIZE))
        arr = np.array(array('h', stream.read(CHUNK_SIZE)))
        repetitions = range(1000)    
        if byteorder == 'big':
            snd_data.byteswap()
            arr.byteswap()

        # Är chunken tyst??
        # Anatime0 = process_time()
        # for xx in  range(2000) :
        # ChunkMaxAmp = AnalyzeChunk(snd_data)

         
        # Anatime = process_time() - Anatime0

        

        # Addera t kön
        # Arrtime0 = process_time()
        # for xx in  range(2000)  :
        # ChunkQ.extend(snd_data)
        # Arrtime = -(Arrtime0 - process_time())
        # ListQ.append(ii,("prp",snd_data))
        # Listtime0 = process_time()
        # for xx in  range(2000)  :
        ListQ.append([( "", "", "", "", "","points", "", "",""),arr])
        # Listtime = -(Listtime0 - process_time())
        y=0
        # TimeList.append([(ii,Anatime, Arrtime,Listtime)])
      
    z=32

    ArrTot0 = array('h')
    for ii in range(1,101) :
        tup = ListQ[ii][0]
        arr = ListQ[ii][1]
        ArrMaxAmp = np.amax(np.absolute(arr))
        ArrMaxNdx = np.argmax(np.absolute(arr)) 
        ArrMean   = round(np.mean(np.absolute(arr)) ) 
        # ArrAverage= np.average(np.absolute(arr))  
        ArrMedian   = np.median(np.absolute(arr))
        ArrMeaDivMed = round(ArrMean/ArrMedian)
        ArrVar   = round(np.var(np.absolute(arr)) )
        ArrStd   = round(np.std(np.absolute(arr)) )
        ArrHistogram= np.histogram(np.absolute(arr))
        ArrTot0.extend(arr)   
        if ArrMaxAmp < THRESHOLD :
            silent = True
        else :
            silent = False
        newtup = (silent, ArrMaxAmp, ArrStd, ArrMeaDivMed, "points", ArrMaxNdx, ArrVar, ArrMean, ArrMedian )

        ListQ[ii][0] = newtup



    x=0
    ArrTot = np.array(ArrTot0)

    ArrMax = [yy[1] for yy in [xx[0] for xx in ListQ]]
    ArrStd = [yy[2] for yy in [xx[0] for xx in ListQ]]
    ArrDiv = [yy[3] for yy in [xx[0] for xx in ListQ]]
    ArrVar = [yy[6] for yy in [xx[0] for xx in ListQ]]
    
    ArrMax[0] = 2000
    ArrStd[0] = 200
    ArrDiv[0] = 1
    ArrVar[0] = 1000
    for ii in range(101) :
        ArrDiv[ii] = ArrDiv[ii] * 1000
        ArrVar[ii]  = round(ArrVar[ii] /1000)
    
    data = zip(ArrMax,ArrStd)
    
    plt.figure(1)
    plt.title('Audio Silence  ...')
    # plt.scatter(*zip(*data))
    plt.xlabel('ArrMax')
    plt.ylabel('ArrStd')
    # data = ListQ
    # x_val = [ArrMax for y in data]
    # y_val = [ArrStd for y in data]
    t = np.arange(0.,130.,10.,)


    plt.plot(ArrDiv,'bs')
    plt.plot(ArrStd,'or')
    plt.plot(ArrMax,'g^')
    plt.plot(ArrVar,'k--^')


    plt.figure(2)

    plt.plot(ArrTot)


    #plt.plot(data,'or')
    plt.show()
    # plt.plot(ListQ[][0],ListQ[][2],ListQ[][3])
  
   
    # plt.show()

    # filen = file.replace(".wav",".png")
    # plt.savefig(filen, bbox_inches='tight')
    # filen = filen.replace(".pdf",".png")
    # plt.savefig(filen, bbox_inches='tight')

    plt.close()

    rr = 0

# ringbuff_numpy_test()

listen()