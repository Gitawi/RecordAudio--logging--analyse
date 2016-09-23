import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
from os  import listdir
# from scandir
# scandir


Directory = "E:\Git\RecordAudio\slask\\"

for file in listdir(Directory):
    if file.endswith(".wav")  :
        file = Directory + file
        # print(os.path.join(directory, filename))
 
        spf = wave.open(file,'rb')

        #Extract Raw Audio from Wav File
        signal = spf.readframes(-1)
        signal = np.fromstring(signal, 'Int16')
        fs = spf.getframerate()

        #If Stereo
        if spf.getnchannels() == 2:
            print( 'Just mono files')
            sys.exit(0)

        Time=np.linspace(0, len(signal)/fs, num=len(signal))

        plt.figure(1)
        plt.title('Signal Wave...')
        plt.plot(Time, signal)
        # plt.show()

        filen = file.replace(".wav",".png")
        plt.savefig(filen, bbox_inches='tight')
        # filen = filen.replace(".pdf",".png")
        # plt.savefig(filen, bbox_inches='tight')

        plt.close()



        continue
    else:
        continue

