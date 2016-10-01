import numpy as np
from sys import byteorder
from array import array
from struct import pack
from time import process_time
import datetime
import time
import matplotlib.pyplot as plt
import csv
#from numpy import fft


import pyaudio
import wave
import timeit
import logging

logger = logging.getLogger('testmodule')
def loggsetup(logger) :
    
    logger.setLevel(logging.DEBUG)

    """
    Loggar till 2 filehandles, en fil och en stderror
    """

    # create file handler which logs even debug messages
    fh = logging.FileHandler('slask\\'+str(datetime.datetime.fromtimestamp(time.time()).strftime('%y%m%d %H%M%S'))+".log")
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Formatter 2 nedan är bäst


    # create formatter with '{'-str.format()  formatting style and add it to the handlers - Verkar bäst
    formatter2 = logging.Formatter('{asctime}/{name}/{lineno:0=3}/{levelname:9}{message}', datefmt='%y%m%d/%H:%M:%S', style='{')
    ch.setFormatter(formatter2)
    fh.setFormatter(formatter2)
    logger.addHandler(ch)
    logger.addHandler(fh)


    # logger.debug('debug message formatter2')
    # logger.info('info message formatter2')
    # logger.warn('warn message formatter2')
    # logger.error('error message formatter2')
    # logger.critical('critical message formatter2')

    logger.info("ProgramRun Started" )
    logger.info("THRESHOLD_START ="+ str(THRESHOLD_START)  +  "\t THRESHOLD_CONT =" + str(THRESHOLD_CONT)  )
    logger.info("CHUNKS_NOOF =" +  str(CHUNKS_NOOF) +  "\t CHUNK_SIZE =" +  str(CHUNK_SIZE) +  "\t RATE =" + str(RATE)   )
    logger.info("PLOT_SCALE =" +  str(PLOT_SCALE) +  "\t PLOT_DPI =" +  str(PLOT_DPI) +  "\t PLOT_FIGSIZE =" +  str(PLOT_FIGSIZE) )
    logger.info("WAVE_ENDADDS =" +  str(WAVE_ENDADDS) + "\t SAVE_TO_DIR =" +  str(SAVE_TO_DIR) +  "\t RUN_START =" +  str(RUN_START) + "\n\n" )


"""
Ställ in hur många chunks om 1024 som skall köras, 10 - ngn tiondels sekund,-1000 några sekunder
Ändra ev några andra inputvariabler,
Sedan spelar programmet in dessa, beräknar ett antal varabler på chunkdatan.
Exporterar dessa som en csv-filter
Presenerar ett urval som en graph - ett värde per chunk.
Summerar chunkarna till en ljudfil
Presenterar ljudfilen som graf och som en wav-filterAll export går till /slask under main directoriet  
"""

"""
Tidsfördelning 1000 chunks
Recording
Recording klart: 23.2027secs     chunks:1000 chunks/sec:43
Analys
Analys klart: 1.3448secs     chunks:1000 chunks/sec:744
Close pyAudio
Close klart: 18.0925secs     chunks:1000 chunks/sec:55
Cvs export
Cvs klart: 4.8984secs     chunks:1000 chunks/sec:204
Plot
Plot klart: 2.897secs     chunks:1000 chunks/sec:345
Wave export
Wav klart: 15.8343secs     chunks:1000 chunks/sec:63

"""
"""
Analysen
Det verkar som att i stort sett alla mätvärden hoppar till vid höga ljud, dock mest 
MaxLjudamplitud och variansen

Sen planar det ut under c:a 5-10 1024=chunkar för att sen återgå till normalläget.
Man skall nog fortsätta spel in så länge normalläget inte återkommit och då verkar
Variansen och kanske standardavvikelsen vara lämpliga

Kanske bra att spara csv-filen med data och en graf med varje inspelning tills vidare.
    kanske man också skall spara det som legat nära i början för att lära sig
"""


# Settings during the run

# Autorecording choices, seconds
THRESHOLD_START = 5500
THRESHOLD_CONT = 1500
# File size & Quality etc
CHUNKS_NOOF = 10 # Hur läng skall det lyssnas, antal CHUNKS_NOOF = CHUNK_SIZE
RATE = 8000
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
WAVE_ENDADDS = 0.5

PLOT_SCALE = 1000
PLOT_FIGSIZE = (22,7)
PLOT_DPI = 100
SAVE_TO_DIR = "slask\\"
RUN_START = str(datetime.datetime.fromtimestamp(time.time()).strftime('%y%m%d %H %M %S'))



# # Autorecording choices, seconds
# THRESHOLD_START = 7000
# # THRESHOLD = 7000
# THRESHOLD_CONT = 1500
# SAVE_TO_DIR = "slask\\"
# # RunStart = 

# # pyaudio settings
# CHUNK_SIZE = 1024
# FORMAT = pyaudio.paInt16
# # FORMAT = np.int16
# MAXIMUM = 16384
# RATE = 8000
# # RATE = 44100
# ARRAYTYPE = array('h') 


def timing(Title, onoff) :
    # För att tima löptid genom ett program
    # annars kör timeit för detaljtest med repetitioner
    # Always time.clock() on windows
    if onoff == "on" :
        timing.LastTime = time.clock()
        logger.info(Title )
    elif onoff == "off" :
        tid = time.clock() - timing.LastTime
        Chunksrate = round(CHUNKS_NOOF/tid)
        logger.info(Title + " klart: " + str(round(tid,4)) + "secs " )
    else : 
        logger.error("on/off saknas i timing-argumenten")
timing.LastTime = 0.0 # Hör till functionsobjectet "timing som en property. Måste initialiseras"




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
            if not snd_started and abs(i)>THRESHOLD_START:
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


def listen() :
     # Startar pyAudio
    p = pyaudio.PyAudio()
    # Öppnar en p.stream
    stream = p.open(format = FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)
    ListQ = []
    ListQ.append([["", "Max", "Std", "ArrTid" , "SekvTime", "arg", "Var", "Mean", "Median"],"Histo","Arr"])
    # TimeList = [["ii", "Anatime","Arrtime", "Listtime"]]

    
    #  loopen med inspelning
    OldTime = ListQTime = time.time()
    ProspNdxOn = -1
    timing("Recording", "on")
    for ii in range(1,CHUNKS_NOOF) :
        arr = np.array(array('h', stream.read(CHUNK_SIZE)))
        if byteorder == 'big':
            snd_data.byteswap()
            arr.byteswap()
        
        # Initierar med arr-ljuddumpar
        ListQ.append([[ "", "", "", time.time(),"", "" ,"", "", ""],"",arr])

    timing("Recording", "off")

      
    # Analysera Listan med ljud, per dump och slå ihop en hel ArrTot
    # ArrTot0 = array('h')
    # ArrVarAcc = 0
    MaxArrMax = MinArrMax = MaxArrVar = MinArrVar = MaxArrStd = MinArrStd = 0
    Spara = 0
    # AnaTime = time.time()
    timing("Analys", "on")
    for ii in range(1,CHUNKS_NOOF) :
        tup = ListQ[ii][0]
        arr = ListQ[ii][2]
        ArrMaxAmp = np.amax(np.absolute(arr))
        MaxArrMax = max(MaxArrMax,ArrMaxAmp)
        MinArrMax - min(MinArrMax,ArrMaxAmp) 
        ArrMaxNdx = np.argmax(np.absolute(arr)) 
        ArrMean   = round(np.mean(np.absolute(arr)) ) 
        ArrMedian   = np.median(np.absolute(arr))
        #ArrMeaDivMed = round(ArrMean/ArrMedian)
        ArrVar   = round(np.var(np.absolute(arr)) )
        MaxArrVar = max(MaxArrVar,ArrVar)
        MinArrVar - min(MinArrVar,ArrVar) 
        #ArrVarTip = ArrVar/ArrVarAcc*1000
        # ArrVarAcc += ArrVar/5
        ArrStd   = round(np.std(np.absolute(arr)) )
        MaxArrStd = max(MaxArrStd,ArrStd)
        MinArrStd - min(MinArrStd,ArrStd) 
        ArrHistogram= np.histogram(np.absolute(arr))
        ArrTid = str(datetime.datetime.fromtimestamp(tup[3]).strftime('%y%m%d %H%M%S'))
        SekvTime =  tup[3] - OldTime
        OldTime = tup[3]
          
        ListQ[ii]  = [["", ArrMaxAmp, ArrStd, ArrTid , SekvTime,  ArrMaxNdx, ArrVar, ArrMean, ArrMedian], ArrHistogram,arr]
    
        RepTxt = ""
        # Start recording?
        if ArrMaxAmp < THRESHOLD_START :
            RepTxt = RepTxt + "Silent, "
            Spara -= 1
        else :
            RepTxt = RepTxt + "Sound, "
            Spara = max(Spara, 10)
            if ProspNdxOn < 0 :
                ProspNdxOn = ii 
                RepTxt =  "Spara = 10 " + RepTxt
            
        # ListQ[ii][0][0] = RepTxt


        # Continu Listening?
        if ii > THRESHOLD_CONT :
            RepTxt = RepTxt + ", ii=" + str(ii) 
            ListQ[ii][0][0] = RepTxt
            logger.warning("ToLong - Break")
            break

        # Continue recording?
        if Spara > 2 :
                RepTxt = "Sparar " + str(Spara) + " " + RepTxt
        elif Spara > 0:
            VarLev = (ArrVar - MinArrVar)/(MaxArrVar - MinArrVar)
            StdLev = (ArrStd - MinArrStd)/(MaxArrStd - MinArrStd)
            if VarLev + StdLev  > THRESHOLD_CONT :
                RepTxt =  "Spara,  Öka till 3, " + RepTxt
                Spara = max(Spara,3)
            else:
                RepTxt = "Sparat klart "
                for xx in range((ProspNdxOn-3),ProspNdxOn) :
                    ListQ[xx][0][0] = "Sparar före  " + ListQ[xx][0][0]
                ProspNdxOn = -1
        ListQ[ii][0][0] = RepTxt


    timing("Analys", "off")


    # Stopp pyAudio stream etc 
    timing("Close pyAudio", "on")
    stream.stop_stream()
    stream.close()
    p.terminate()
    timing("Close pyAudio", "off")




    # Export data to csv, 
    timing("Cvs export", "on")

    filename = SAVE_TO_DIR + str(datetime.datetime.fromtimestamp(ListQTime).strftime('%y%m%d %H%M%S')) + ".csv"
    tuple = [xx[0] for xx in ListQ] 
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(tuple)

    timing("Cvs export", "off")
  

    # Build total wave file
    ListQ[0][2] = ListQ[1][2]
    ArrTot0 = array('h')
    # ArrTot0.extend([yy[1] for yy in ListQ])
    for ii in range(CHUNKS_NOOF) :
        ArrTot0.extend(ListQ[ii][2]) 
    ArrTot = np.array(ArrTot0)
    ArrTot = normalize(ArrTot)
    ArrTot = trim(ArrTot)



    # Prepare for plottin
    timing("Plot", "on")
    ArrMax = [yy[1] for yy in [xx[0] for xx in ListQ]]
    ArrStd = [yy[2] for yy in [xx[0] for xx in ListQ]]
    # ArrDiv = [yy[3] for yy in [xx[0] for xx in ListQ]]
    # ArrVarTip= [yy[4] for yy in [xx[0] for xx in ListQ]]
    ArrVar = [yy[6] for yy in [xx[0] for xx in ListQ]]



    
    ArrMax[0] = 2000
    ArrStd[0] = 200
    # ArrDiv[0] = 1
    ArrVar[0] = 1000
    # ArrVarTip[0] = 1000
    # Scale the variables
    # Scale = 1000
    for ii in range(CHUNKS_NOOF) :
        ArrMax[ii] = round(ArrMax[ii]/MaxArrMax * PLOT_SCALE)
        ArrVar[ii] = round(ArrVar[ii]/MaxArrVar * PLOT_SCALE)
        ArrStd[ii] = round(ArrStd[ii]/MaxArrStd * PLOT_SCALE)
        
    # ArrVar[ii]  = round(ArrVar[ii] /1000)
    
    plt.figure(1, figsize=PLOT_FIGSIZE, dpi=PLOT_DPI)
    plt.title('Audio nyckelvärden  ... ' + str(datetime.datetime.fromtimestamp(ListQTime).strftime('%y%m%d %H%M%S')))
    # plt.xlabel('ArrMax')
    # plt.ylabel('ArrStd')

    # plt.plot(ArrDiv,'bs')
    plt.plot(ArrStd,'r-', label = "Stdavvikelse")
    plt.plot(ArrMax,'b-' ,label = "Ampmax")
    plt.plot(ArrVar,'k-' ,label = "Variance")
    plt.legend(loc='upper left')
    # for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
    #          ax.get_xticklabels() + ax.get_yticklabels()):
    #     item.set_fontsize(20)
    # plt.plot(ArrVarTip,'r:^')
    # Spara plotten som fil
    filen = filename.replace(".csv","-1.png")
    plt.savefig(filen, bbox_inches='tight')

    plt.figure(2, figsize=PLOT_FIGSIZE, dpi=PLOT_DPI)
    plt.title('Audio filen  ... ' + str(datetime.datetime.fromtimestamp(ListQTime).strftime('%y%m%d %H%M%S')))
    plt.plot(ArrTot)
    filen = filename.replace(".csv","-2.png")
    plt.savefig(filen, bbox_inches='tight')


  # Visa bådda figures
    #plt.show()


    plt.close()

    timing("Plot", "off")

 
 
    timing("Wave export", "on")

    # OBS  plt.plot(ArrTot) klarar inte att plotta ArrTot om den packats först, krashar
    ArrTot = add_silence(ArrTot, WAVE_ENDADDS)   # Here not to affect the plots
    sample_width = p.get_sample_size(FORMAT)
    ArrTot = pack('<' + ('h'*len(ArrTot)), *ArrTot)
    # OBS  plt.plot(ArrTot) klarar inte att plotta ArrTot om den packats först


    filen = filename.replace(".csv",".wav")
   
    wf = wave.open(filen, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(ArrTot)
    wf.close()

    timing("Wave export", "off")


 # Visa båda figures
    # plt.show()


  



   

    rr = 0 # Stanna upp en stund
loggsetup(logger)
# RunTimeData()
listen()


