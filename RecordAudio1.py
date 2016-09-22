# down voteAs a follow up to Nick Fortescue's answer, here's a more complete example of how to record from the microphone and process the resulting data:
# To make this work in Python 3 just replace range with range. – Ben Elgar Feb 23 '15 at 22:52

from sys import byteorder
from array import array
from struct import pack
import time
import datetime

import pyaudio
import wave

# THRESHOLD = 500
THRESHOLD = 10000

CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100

def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    #print(max(snd_data), end=", ", flush=True)
    return max(snd_data) < THRESHOLD

def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)
    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
        
    return r

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

def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    r = array('h', [0 for i in range(int(seconds*RATE))])
    r.extend(snd_data)
    r.extend([0 for i in range(int(seconds*RATE))])
    return r

def record():
    
    """
    Record a word or words from the microphone and 
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the
    start and end, and pads with 0.5 seconds of   
     blank sound to make sure VLC et al can play 
    it without getting chopped off.
    """
    # Startar pyAudio
    p = pyaudio.PyAudio()
    # Öppnar en p.stream
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)

    # Nollar startvärden
    num_silent = 0
    snd_started = False
    snd_data = array('h', stream.read(CHUNK_SIZE))
    if byteorder == 'big':
            snd_data.byteswap()
    # ... och ljudarrayen
    r = array('h')

    # Startar loopen
    tiden = time.time()
    Timestamp = str(datetime.datetime.fromtimestamp(tiden).strftime('%Y%m%d %H:%M:%S'))
    print("\n Into While ... ", Timestamp)
    while 1:
        # little endian, signed short
        # Laddar en chunk ur streamen till snd_data
        # fortsätter streamen recorda??
        snd_dataold = snd_data
        snd_data = array('h', stream.read(CHUNK_SIZE))
        
        if byteorder == 'big':
            snd_data.byteswap()

       

        # r chunken tyst??
        silent = is_silent(snd_data)

        # Testa nya chunken
        if snd_started: 
            # Lägg sista chunken till r - ljudarrayen
            r.extend(snd_dataold)    
            r.extend(snd_data)
            if silent:
                num_silent += 1
            else:
                num_silent = 0
        else:
            if not silent:
                snd_started = True
                # Addera sista chunken till r - ljudarrayen    
                r.extend(snd_data)
                tiden = time.time()
                Timestamp = str(datetime.datetime.fromtimestamp(tiden).strftime('%Y%m%d %H:%M:%S'))
                print(" snd_started    ", Timestamp)
                
                

        # if silent and snd_started:   # Slut på ljud under inspelning
        #     num_silent += 1
        # elif not silent and not snd_started: # Ljud:-> Starta inspelning
        #     snd_started = True 
        # elif snd_started: # Ljud:-> Starta inspelning
        #     snd_started = True
            

        if snd_started and num_silent > 500: # Varit tyst länge nu ...
            tiden = time.time()
            Timestamp = str(datetime.datetime.fromtimestamp(tiden).strftime('%Y%m%d %H:%M:%S'))
            print(" Tyst för länge ", Timestamp)
            break


    
        
        
    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    # r = normalize(r)
    # r = trim(r)
    # r = add_silence(r, 0.5)
    return sample_width, r

def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    # print("In record_to_file")
    # Två returnvalues från record
    sample_width, data = record()

    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()

if __name__ == '__main__':
    #print("please speak a word into the microphone")
    ii = 1
    for ii  in range(99):
        file = "slask\demo{0:02d}.wav".format(ii)
        # print(file, ii)
        record_to_file(file)
        tiden = time.time()
        Timestamp = str(datetime.datetime.fromtimestamp(tiden).strftime('%Y%m%d %H:%M:%S'))
        print(file + " " + Timestamp)
        