from microbit import pin0, sleep, display
import radio #Allows microbits to communicate

RATE = 20
pin0.set_analog_period(RATE)
display.scroll('Hello, World!')  

START_GROUP = 2
CHANNEL = 17
radio.config(group=START_GROUP,queue=1,channel=CHANNEL) #group = channel; queue=1 ensures that the microbits only store a backlog of 1 message rather than storing loads, meaning they can't get clogged up. The microbits are always listening even when doing something else and messages are added to a queue. Here we cap the queue at size 1 message
radio.on() #radio communication is off by default to save power so we need to activate it.

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


location = spoofLocation()
def processRadioCommand(cmd):
    global location
    if cmd[0] == "L": #Location
        lat,lon = next(location)
        return str(lat)+";"+str(lon)

    elif cmd[0] == "M": #Motor
        if cmd[1] == "1":
            setAngle(-60,pin0)
            return "Status,True"
        elif cmd[1] == "2":
            setAngle(60,pin0)
            return "Status,True"
        else:
            return "Status,False"


while True:
    msg = radio.receive()
    if msg != None:
        result = processRadioCommand(msg)
        radio.send(result)

