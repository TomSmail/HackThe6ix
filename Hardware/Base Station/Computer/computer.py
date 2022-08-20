#device manager - ports, com and LPT, usb serial device

import serial
import time

EVERY = 5

ser = serial.Serial()
ser.baudrate = 115200
ser.port = "COM5"
ser.open()

start = time.time()

while True:
    print("waiting")
    microbitdata = str(ser.readline().strip().decode("ascii"))
    values = microbitdata.split(";")
    if len(values) == 1: #got a status
        print(values[0].split(",")[1])
    else:
        print("Lat: " + values[0])
        print("Lon: " + values[1])
    
    now = time.time()
    if (now-start % )

    

