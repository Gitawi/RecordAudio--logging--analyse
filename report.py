import sqlite3
import time
import datetime
import random
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style
style.use('fivethirtyeight')


print("*** Start")
print("connect")
conn = sqlite3.connect("output/TestSQL.DB")
c = conn.cursor()

def create_table ():
    c.execute("CREATE TABLE IF NOT EXISTS Tabell1 (dTiden INT, cTimestamp TEXT, cMaskin TEXT, cProgram TEXT, cItem TEXT, nValue REAL )") 
    ## c.execute("CREATE TABLE Tabell1 (cTimestamp TEXT, cMaskin TEXT, cProgram TEXT, cItem TEXT, nValue REAL )") 


def dynamic_data_entry ():
    for i in range(10):
     
        tiden = time.time()
        Timestamp = str(datetime.datetime.fromtimestamp(tiden).strftime('%Y%m%d %H:%M:%S'))
        mätv = random.randrange(0,10)
        Maskin = "RPy"
        Program = "TestSQL1"
        Variabel = "Fuktighet"
        c.execute( "INSERT INTO Tabell1 (dTiden, cTimestamp, cMaskin, cProgram, cItem, nValue  ) VALUES (?, ?,?,?,?,?)", (tiden, Timestamp, Maskin, Program, Variabel, mätv) )
        time.sleep(1.2)
    conn.commit()
    

def read_from_db(): 
    c.execute("""SELECT dTiden, nValue, cTimestamp FROM Tabell1 """)
    for row in c.fetchall():
        print(row)


def graph_data():
    c.execute("""SELECT dTiden, cTimestamp, nValue FROM Tabell1 """)
    dates = []
    mått = []
    for row in c.fetchall() :
        print(row[0])
        print(row[2])   
        dates.append(datetime.datetime.fromtimestamp( row[0]))
        mått.append(row[2])
        
    # print(dates[0],dates[1],dates[2])
    # print(mått[0],mått[1],mått[2])
        
    plt.plot_date(dates, mått, '-')
    plt.show()
        
        
        
print("***")
print("create")
create_table()
print("***")
print("dynamic")
dynamic_data_entry()
print("***")
print("read")
read_from_db()
print("***")
print("graph")
graph_data()
print("***")
c.close()
conn.close()


