import numpy as np
from sys import byteorder
from sys import getsizeof
from array import array
from struct import pack
from time import process_time
import datetime
import time
import matplotlib.pyplot as plt
import csv
from Loggerdef import loggsetup 
import pyaudio
import wave
import timeit

# Run identification. Use as unique but identifiable filename, ad extension and path
RunID = datetime.datetime.now().strftime('%y%m%d %H%M%S')
# RunID = str(datetime.datetime.fromtimestamp(time.time()).strftime('%y%m%d %H%M%S'))
AppID = "AudioRec"

logger, = loggsetup(RunID,AppID,("multi",))





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
THRESHOLD_AMP = 5500
THRESHOLD_VAR = 30000  # denna verkar ta mer prat än höga ljud
THRESHOLD_STD = 0.27
# File size & Quality etc
CHUNKS_NOOF = 25 # Hur länge skall det lyssnas, antal CHUNKS_NOOF = CHUNK_SIZE
RATE = 8000
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
WAVE_ENDADDS = 0.5

PLOT_SCALE = 1000
PLOT_FIGSIZE = (22,7)
PLOT_DPI = 100
SAVE_TO_DIR = "slask\\"
RUN_START = RunID

logger.info("ProgramRun Started: " + RunID )
logger.info("THRESHOLD_AMP ="+ str(THRESHOLD_AMP)  +  "\t THRESHOLD_STD =" + str(THRESHOLD_STD)  )
logger.info("CHUNKS_NOOF =" +  str(CHUNKS_NOOF) +  "\t CHUNK_SIZE =" +  str(CHUNK_SIZE) +  "\t RATE =" + str(RATE)   )
logger.info("PLOT_SCALE =" +  str(PLOT_SCALE) +  "\t PLOT_DPI =" +  str(PLOT_DPI) +  "\t PLOT_FIGSIZE =" +  str(PLOT_FIGSIZE) )
logger.info("WAVE_ENDADDS =" +  str(WAVE_ENDADDS) + "\t SAVE_TO_DIR =" +  str(SAVE_TO_DIR) +  "\t RUN_START =" +  RunID + "\n\n" )



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
            if not snd_started and abs(i)>THRESHOLD_AMP:
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
    ListQ.append([["Text", "Max", "Std", "ArrTid" , "SekvTime", "arg", "Var", "Mean", "Median"],"Histo","Arr"])
    # TimeList = [["ii", "Anatime","Arrtime", "Listtime"]]

    
    #  loopen med inspelning
    OldTime = ListQTime = time.time()
    ProspNdxOn = -1
    timing("Recording", "on")
    for ii in range(1,CHUNKS_NOOF) :
        if 0 == ii%25 : print(ii,end=' ')
        # if ii == CHUNKS_NOOF : print(ii,)
        arr = np.array(array('h', stream.read(CHUNK_SIZE)))
        if byteorder == 'big':
            snd_data.byteswap()
            arr.byteswap()
        
        # Initierar med arr-ljuddumpar
        ListQ.append([[ "", "", "", time.time(),"", "" ,"", "", ""],"",arr])

    timing("Recording", "off")

      
    # Analysera Listan med ljud, per dump och slå ihop en hel ArrTot
    MaxArrMax = MinArrMax = MaxArrVar = MinArrVar = MaxArrStd = MinArrStd = 0
    Recording = 0
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
        ArrVar   = round(np.var(np.absolute(arr)) )
        MaxArrVar = max(MaxArrVar,ArrVar)
        MinArrVar - min(MinArrVar,ArrVar) 
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
        
        # Filstorlek Listening?
        if 0 == (ii%600) :
            RepTxt = RepTxt + ", ii=" + str(ii) + ", size=" + str(getsizeof(ListQ)) 
            ListQ[ii][0][0] = RepTxt
            logger.warning("Long " + RepTxt)
            # break
        
        if ArrMaxAmp < THRESHOLD_AMP :
            RepTxt = RepTxt + "Silent, "
            Recording -= 1
        else :
            RepTxt = RepTxt + "Sound, "
            Recording = max(Recording, 15)
            if ProspNdxOn < 0 :
                ProspNdxOn = ii 
                RepTxt =  "Recording = "+str(Recording)  + RepTxt
                
        # ListQ[ii][0][0] = RepTxt
        
        # Continue recording?
        VarLev = (ArrVar - MinArrVar)/(MaxArrVar - MinArrVar)
        StdLev = (ArrStd - MinArrStd)/(MaxArrStd - MinArrStd)
        VSSum = VarLev + StdLev
        if Recording > 2 :
                RepTxt = "Sparar " + str(Recording) + " VSSum" + str(VSSum) +"/"+ RepTxt
        elif Recording > 0:
            if VarLev + StdLev  > THRESHOLD_STD :
                RepTxt =  "Recording,  Öka till 5, " + RepTxt
                Recording = max(Recording,5)
            else:
                RepTxt = "Sparat klart "
                for xx in range((ProspNdxOn-5),ProspNdxOn) :
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

    filename = SAVE_TO_DIR + RunID + ".csv"
    tuple = [xx[0] for xx in ListQ] 
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(tuple)

    timing("Cvs export", "off")
  

    # Build total wave file
    ListQ[0][2] = ListQ[1][2]
    ArrTot0 = array('h')
    ArrSpar = arrtmp = array('i')
    ArrChunks=array('h', (aa for aa in range(0,CHUNKS_NOOF*CHUNK_SIZE)))
    for ii in range(CHUNKS_NOOF) :
        ArrTot0.extend(ListQ[ii][2])
        lev = 8000 
        if "Silent" in  ListQ[ii][0][0][0:10] : 
            lev = 0
        arrtmp = array('i',(lev for i in range(0,1024)))
        ArrSpar.extend(arrtmp)

    ArrTot = np.array(ArrTot0)



    # Prepare ListQ for plottin
    timing("Plot", "on")
    ArrMax = [yy[1] for yy in [xx[0] for xx in ListQ]]
    ArrStd = [yy[2] for yy in [xx[0] for xx in ListQ]]
    ArrVar = [yy[6] for yy in [xx[0] for xx in ListQ]]

    
    ArrMax[0] = 100
    ArrStd[0] = 200
    ArrVar[0] = 100
    for ii in range(CHUNKS_NOOF) :
        ArrMax[ii] = round(ArrMax[ii]/MaxArrMax * PLOT_SCALE)
        ArrVar[ii] = round(ArrVar[ii]/MaxArrVar * PLOT_SCALE)
        ArrStd[ii] = round(ArrStd[ii]/MaxArrStd * PLOT_SCALE)
        HorAmp = PLOT_SCALE *THRESHOLD_AMP/MaxArrMax
        HorVar = PLOT_SCALE *THRESHOLD_VAR/MaxArrVar
        HorStd = PLOT_SCALE *THRESHOLD_STD/MaxArrStd
        
    
    logger.info("Plot: Audio nyckelvärden")
    plt.figure(1, figsize=PLOT_FIGSIZE, dpi=PLOT_DPI)
    plt.title('Audio nyckelvärden  ... ' + RunID +"/ "+ AppID)
    plt.plot(ArrStd,'r-', label = "Stdavvikelse")
    plt.plot(ArrMax,'b-' ,label = "Ampmax")
    plt.plot(ArrVar,'k-' ,label = "Variance")
    plt.axhline(y=HorAmp, color = "b")
    plt.axhline(y=HorVar, color = "m")
    plt.axhline(y=HorStd, color = "r")


    plt.legend(loc='upper left')
    filen = SAVE_TO_DIR + RunID + "-1.png"
    plt.savefig(filen, bbox_inches='tight')

    logger.info("Plot: Audio filen")
    plt.figure(2, figsize=PLOT_FIGSIZE, dpi=PLOT_DPI)
    plt.title('Audio filen  ... ' + RunID +"/ "+ AppID)
    plt.plot(ArrChunks,np.absolute(ArrTot))
    plt.plot(ArrSpar,'m-', label="Recording")
    plt.axhline(y=THRESHOLD_AMP)    
    # plt.xaxis.set_major_locator(plt.MultipleLocator(10*CHUNK_SIZE))
    plt.plot(ArrChunks,'c^')
    plt.ylim(-100,15000)
    filen = SAVE_TO_DIR + RunID + "-2.png"
    plt.savefig(filen, bbox_inches='tight')

    logger.info("Plot: Audio histogram")
    plt.figure(3, figsize=PLOT_FIGSIZE, dpi=PLOT_DPI)
    # width = 0.7 * (bins[1] - bins[0])
    # center = (bins[:-1] + bins[1:]) / 2
    plt.hist(np.absolute(ArrTot),50)
    plt.title(('Histogram   ... {0}/  {1}').format( RunID, AppID))
    filen = SAVE_TO_DIR + RunID + "-3.png"
    plt.savefig(filen, bbox_inches='tight')

  # Visa bådda figures
    #plt.show()


    plt.close()

    timing("Plot", "off")

 
 
    timing("Wave export", "on")

    # OBS  plt.plot(ArrTot) klarar inte att plotta ArrTot om den packats först, krashar
    # ArrTot = normalize(ArrTot)
    #ArrTot = trim(ArrTot) #(för att inte förstöra indexet mellan plot och csv-fil)
    #ArrTot = add_silence(ArrTot, WAVE_ENDADDS)   # Here not to affect the plots
    sample_width = p.get_sample_size(FORMAT)
    #ArrTot = pack('<' + ('h'*len(ArrTot)), *ArrTot)
    # OBS  plt.plot(ArrTot) klarar inte att plotta ArrTot om den packats först


    filen = SAVE_TO_DIR + RunID + ".wav"
   
    wf = wave.open(filen, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(ArrTot)
    wf.close()

    timing("Wave export", "off")



    rr = 0 # Stanna upp en stund

listen()


