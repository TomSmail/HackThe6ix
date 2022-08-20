from microbit import pin0, sleep, display

RATE = 20
pin0.set_analog_period(RATE)
display.scroll('Hello, World!')  

def setAngle(angle):
    if (angle > 90 or angle < -90):
        return False
    duty_time = angle/180 + 1.5
    pin0.write_analog(duty_time*1000/RATE)
    
    return True

while True: 
    setAngle(-60)
    sleep(1000)
    setAngle(60)
    sleep(1000)

    