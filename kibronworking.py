
#This is a very simple script on how to communicate with the sensor 

import serial
import struct
import time
import csv

comport='COM4' # set your connected port
GetData = b'\x02\x0a\xf0\x41\xf1\x03' 
sleepInterval = 1 #seconds

data = {}
rows = []

fieldnames = ["date", "time (s)","temperature","pressure","tension"]
createNewFile = True
fileName = 'data'
fileExtension = '.txt'
timeStr = time.strftime("%Y%m%d-%H%M%S")
initialTime = time.time_ns()
    
def getRelativeTime(currentTime):
    return ((currentTime - initialTime)//1000000)/1000
def readSensor():
    sen.write( GetData )
    a=''
    while sen.inWaiting() < 4: #Wait for length of return message
        time.sleep(0.0001)
    a=sen.read(4)

    #print("Length of reply is", a, a[3]-64 )
    while sen.inWaiting()< a[3]-64+1:  #Wait for all bytes in reply
       # print(sen.inWaiting())
        time.sleep(0.0001)
    b=sen.read(a[3]-64+1)
    currentTime = time.time_ns()
    #print("Complete byte string from sensor is", a+b)
    #Time to get data from string by converting bytes to floats.
    i=0
    voltage=struct.unpack('>f', b[i:i+4])[0]
    i=4
    tension=struct.unpack('>f', b[i:i+4])[0]
    i=8
    pressure=struct.unpack('>f', b[i:i+4])[0]
    i=12
    temperature=struct.unpack('>f', b[i:i+4])[0]
   
    seconds = time.time()
    print("Tension= %.2f\n" % tension,"Pressure= %.2f\n" % pressure,"Temperature= %.2f\n" %temperature)       #voltage,tension, pressure are all related, and origin from the force sensor.
    return {"date":time.ctime(seconds), "time (s)": getRelativeTime(currentTime),"temperature":temperature, "pressure":pressure, "tension":tension}
def write():
    if createNewFile:
        csvname = fileName +  timeStr + fileExtension
    else:
        csvname = fileName + fileExtension

    with open(csvname, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
def updateRows():
    if data:
        rows.append(data)

sen = serial.Serial(comport, baudrate = 115200)
#  This is octadecimal in python  GetData=b'\2\10\240\65\241\3'. Use e.g. hexa:
i = 0
while True:
    data = readSensor()
    updateRows()
    write()
    timeDiff =  time.time_ns() - initialTime
    sleepTime = max(0,(i+1)*sleepInterval - timeDiff/1_000_000_000)
    time.sleep(sleepTime) # Do some
    i = i+1

