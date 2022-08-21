from microbit import pin0, sleep, display
import radio #Allows microbits to communicate
from drone_pb2_onboard import locationResponse,insecticideResponse,whichRequestType

import sys
def setAngle(angle,pin):
    """Set the servo to a particular angle from -90 to +90 degrees"""
    if (angle > 90 or angle < -90):
        return False
        
    duty_time = angle/180 + 1.5 #1 ms = -90 degrees; 2ms = +90 degrees
    pin.write_analog(duty_time*1000/RATE) # convert using the set rate
    
    return True

def spoofLocation():
    """Spoof location as:
    a) Microbit does not have GPS; custom PCB would
    b) We are not in Canada for testing!
    """

    lat = 56.1304
    lon = -106.3468
    STEP_Lat = 0.01
    STEP_Lon = -0.01
    
    while True:
        yield(lat,lon)
        lat += STEP_Lat
        lon += STEP_Lon

def getDroneLocation():
    global location
    return next(location)

outOfJuice = False
currAngle = 60

def processRadioCommand(cmd):
    global location
    global outOfJuice
    global currAngle
    
    type = whichRequestType(msgBytes)
    if type == 1:
        print("location")
        lat,lon = getDroneLocation()
        bytesOut = locationResponse(lat,lon)
    
    elif type == 2:
        print("servo")
        if outOfJuice:
            bytesOut = insecticideResponse(False,True)
        else:
            bytesOut = insecticideResponse(True,True)
        
        if currAngle == 60:
            currAngle = -60
        elif currAngle == -60:
            currAngle = 60

        setAngle(currAngle,pin0)
        
    return bytesOut


RATE = 20
pin0.set_analog_period(RATE)
display.scroll('Hello, World!')  

START_GROUP = 2
CHANNEL = 17
radio.config(group=START_GROUP,queue=1,channel=CHANNEL,length=100) #group = channel; queue=1 ensures that the microbits only store a backlog of 1 message rather than storing loads, meaning they can't get clogged up. The microbits are always listening even when doing something else and messages are added to a queue. Here we cap the queue at size 1 message
radio.on() #radio communication is off by default to save power so we need to activate it.


location = spoofLocation()

while True:
    msgBytes = radio.receive_bytes()
    if msgBytes != None:
        display.scroll("Received message")
        #result = processRadioCommand(msgBytes)
        print(repr(result))
        radio.send_bytes(result)
        




