# down voteAs a follow up to Nick Fortescue's answer, here's a more complete example of how to record from the microphone and process the resulting data:
# To make this work in Python 3 just replace range with range. – Ben Elgar Feb 23 '15 at 22:52

from sys import byteorder
from array import array
from struct import pack
import time
import datetime

import pyaudio
import wave

# Autorecording choices, seconds
THRESHOLD = 7000
TimeBeforeStart = 3
TimeAfterEnd = 3
AudioSaveToPath = "slask\\"


# pyaudio settings
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
MAXIMUM = 16384
RATE = 44100
ARRAYTYPE = array('h')


def timestamp():
    return time.time()
def filenamestamp():
    return str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d %H%M%S'))
def printablestamp ():
    return str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d %H:%M:%S'))
         
def AnalyzeChunk(snd_data): # former is_silent
    "Returns 'True' if below the 'silent' threshold"
    #print(max(snd_data), end=", ", flush=True)
    return max(snd_data) # < THRESHOLD
    


def normalize(snd_data):
    "Average the volume out"
    scale = float(MAXIMUM)/max(abs(i) for i in snd_data)
    r = ARRAYTYPE
    for i in snd_data:
        r.append(int(i*scale))  
    return r

def add_silence(snd_data, seconds):
    """ 
    pads with 0.5 seconds of   
    blank sound to make sure VLC et al can play 
    it without getting chopped off
    """
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    r = array('h', [0 for i in range(int(seconds*RATE))])
    r.extend(snd_data)
    r.extend([0 for i in range(int(seconds*RATE))])
    return r

def AnalyzeChunkQ(ChunkQ, CQstart, CQend) :
    return



def listen():
    
    """
    Listens to room, acts when noicy
    """
     # Initierar ljudarrayen
    r = array('h')
    rtyst = array('h')
    rextended = 0
    ChunkQ = array('h')
    ChunkIndex = ARRAYTYPE
    CQstart = 0
    CQend = 0

    
    listen = True
    while listen :
        
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
                snd_data.byteswap()

        # Nollar startvärden
        num_silent = 0
        snd_started = False
        strandprospect = 0
      
        # Startar loopen
        # tiden = time.time()
        # Timestamp = str(datetime.datetime.fromtimestamp(tiden).strftime('%Y%m%d %H:%M:%S'))
        print("\n Into While ... ", printablestamp())
        while 1:
            # little endian, signed short
            # Laddar en chunk ur streamen till snd_data
            # fortsätter streamen recorda??
            # snd_dataold = snd_data
            snd_data = array('h', stream.read(CHUNK_SIZE))
            
            if byteorder == 'big':
                snd_data.byteswap()

             # Är chunken tyst??
            ChunkMaxAmp = AnalyzeChunk(snd_data)
          
            if ChunkMaxAmp < THRESHOLD :
                silent = True
            else :
                silent = False

            # Addera t kön
            ChunkQ.extend(snd_data)
            CQstart = 0
            ChunkIndex.append(ChunkMaxAmp)      
            CQend += 1 # CHUNK_SIZE
            if len(ChunkQ) > 8 * CHUNK_SIZE :
                Qstrand = ChunkQ[ : 4 * CHUNK_SIZE]
                ChunkQ = ChunkQ[5 * CHUNK_SIZE :  : ]
                CQend -= 5
                ChunkIndex = 
            


            #AnalyzeChunkQ(ChunkQ, CQstart, CQend)
            
          
            # Testa nya chunken
            if silent:
                strandprospect -= 1
            else :
                if strandprospect < 1:
                    strandstart = CQend
                    strandstarttime = time.time()
                    print("strandprospekt started    ")
                
                strandprospect += 15


            # Testa om dags att skilja ut eller rensa
        
            if strandprospect < 1 :
                CQend - strandstart > 15
                # Skilj ut prospekt

            if strandstart > 100
                # rensa

            if len(ChunkQ) > 100000
                # tvångsskilj strandprospect
                # rensa
                


           



            # # Testa nya chunken
            # if snd_started: 
            #     # Lägg sista chunken till r - ljudarrayen
            #     # r.extend(snd_dataold)    
            #     # r.extend(snd_data)
            #     # rextended += 1
            #     if silent:
            #         num_silent += 1
            #         rtyst.extend(snd_data)
            #     else:
            #         r.extend(rtyst)
            #         rextended += num_silent
            #         num_silent = 0
            #         rtyst = array('h')
            #         r.extend(snd_data)
            #         rextended += 1
            # else:
            #     if not silent:
            #         snd_started = True
            #         filenametime = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d %H%M%S - ')).lstrip("20")
            #         Soundstart = time.time()
        
            #         # Addera sista chunken till r - ljudarrayen    
            #         r.extend(snd_data)
            #         rextended += 1
            #         tiden = time.time()
            #         Timestamp = str(datetime.datetime.fromtimestamp(tiden).strftime('%Y%m%d %H:%M:%S'))
            #         print(" snd_started    ", Timestamp)
                    
        

            # if snd_started and num_silent > 500: # Varit tyst länge nu ...
            #     tiden = time.time()
            #     Timestamp = str(datetime.datetime.fromtimestamp(tiden).strftime('%Y%m%d %H:%M:%S'))
            #     print(" Tyst för länge ", Timestamp)
            #     Soundend = time.time()
            #     Secs = Soundend-Soundstart
            #     print(" Secs{0:02f}, rextended {1:02d}".format( Secs, rextended))
            #     # if Secs > 25 :
            #     #     break
            #     if rextended > 5 : # 25 var OK
            #         listen = False
            #     break
  
        
    sample_width = p.get_sample_size(FORMAT)
    
    to_file(r, sample_width, filenametime)



def to_file (data, sample_width, filenametime):
    data = normalize(data)
    # r = trim(r)
    data = add_silence(data, 0.5)
    # return sample_width, r, filenametime
    data = pack('<' + ('h'*len(data)), *data)

    # filenametime

    filename = AudioSaveToPath + filenametime + "audiorec.wav"
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()
    tiden = time.time()
    Timestamp = str(datetime.datetime.fromtimestamp(tiden).strftime('%Y%m%d %H:%M:%S'))
    print(filename + " " + Timestamp)





if __name__ == '__main__':
    #print("please speak a word into the microphone")
     # Startar pyAudio
    p = pyaudio.PyAudio()
    # Öppnar en p.stream
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)

    ii = 1
    for ii  in range(99):
        listen()


    stream.stop_stream()
    stream.close()
    p.terminate()



def trim(snd_data):
      
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data



       
        