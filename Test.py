import datetime
import time
import io
import sys
import Loggare2
import logging
#  import initialize_logging 


# Setting up globals
# Autorecording choices, seconds
THRESHOLD_START = 5500
THRESHOLD_CONT = 1500
# File size & Quality etc
CHUNKS_NOOF = 10 # Hur läng skall det lyssnas, antal CHUNKS_NOOF = CHUNK_SIZE
RATE = 8000
CHUNK_SIZE = 1024
# FORMAT = pyaudio.paInt16
WAVE_ENDADDS = 0.6

PLOT_SCALE = 1000
PLOT_FIGSIZE = (22,7)
PLOT_DPI = 100
SAVE_TO_DIR = "slask\\"
RUN_START = str(datetime.datetime.fromtimestamp(time.clock()).strftime('%y%m%d %H %M %S'))


# Alternativ output - memory FileExistsError
memstr = io.StringIO("printstart")    

fileh = open("myfile.txt", "w", encoding="utf-8")


def Report(ff) :
    print(memstr.getvalue(), file=ff)
    # memstr.close()



# Reporting (printing) globals
def RunTimeData () : 
    Loggare2.basicConfig(filename="slask\\RUN_START.log", level=Loggare2.DEBUG)

    print("THRESHOLD_START =", THRESHOLD_START , "\t THRESHOLD_CONT =",THRESHOLD_CONT , file=memstr )
    print("CHUNKS_NOOF =", CHUNKS_NOOF, "\t CHUNK_SIZE =", CHUNK_SIZE, "\t RATE =",RATE , file=memstr  )
    print("PLOT_SCALE =", PLOT_SCALE, "\t PLOT_DPI =", PLOT_DPI, "\t PLOT_FIGSIZE =", PLOT_FIGSIZE , file=memstr )
    print("WAVE_ENDADDS =", WAVE_ENDADDS,"\t SAVE_TO_DIR =", SAVE_TO_DIR, "\t RUN_START =", RUN_START , file=memstr )



    xx=0

RunTimeData ()
# Report(memstr)
Report(fileh)
fileh.flush()
Report(sys.stdout)


