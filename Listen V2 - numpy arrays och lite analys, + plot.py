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
    # TimeList = [["ii", "Anatime","Arrtime", "Listtime"]]

    
    # Starta loopen med inspelning
    for ii in range(100) :
        arr = np.array(array('h', stream.read(CHUNK_SIZE)))
        if byteorder == 'big':
            snd_data.byteswap()
            arr.byteswap()
        
        # Initierar med arr dumpar
        ListQ.append([( "", "", "", "", "","points", "", "",""),arr])
      
    # Analysera Listan med ljud, per dum och slå ihop en hel ArrTot
    ArrTot0 = array('h')
    for ii in range(1,101) :
        tup = ListQ[ii][0]
        arr = ListQ[ii][1]
        ArrMaxAmp = np.amax(np.absolute(arr))
        ArrMaxNdx = np.argmax(np.absolute(arr)) 
        ArrMean   = round(np.mean(np.absolute(arr)) ) 
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
    ArrTot = np.array(ArrTot0)


    # Prepare for plottin
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
    
    plt.figure(1)
    plt.title('Audio nyckelvärden  ...')
    plt.xlabel('ArrMax')
    plt.ylabel('ArrStd')

    plt.plot(ArrDiv,'bs')
    plt.plot(ArrStd,'or')
    plt.plot(ArrMax,'g^')
    plt.plot(ArrVar,'k--^')


    plt.figure(2)
    plt.title('Audio filen  ...')
    plt.plot(ArrTot)

    # Visa bådda 
    plt.show()

    # # Spara som fil
    # filen = file.replace(".wav",".png")
    # plt.savefig(filen, bbox_inches='tight')
    # filen = filen.replace(".pdf",".png")
    # plt.savefig(filen, bbox_inches='tight')

    plt.close()

    rr = 0 # Stanna upp en stund

# ringbuff_numpy_test()

listen()