from microbit import button_a, button_b, display
import radio
import time

START_GROUP = 2
CHANNEL = 17
radio.config(group=START_GROUP,queue=1,channel=CHANNEL) #group = channel; queue=1 ensures that the microbits only store a backlog of 1 message rather than storing loads, meaning they can't get clogged up. The microbits are always listening even when doing something else and messages are added to a queue. Here we cap the queue at size 1 message
radio.on() #radio communication is off by default to save power so we need to activate it.
DELAY = 1

servo_on = False

while True:
    if button_a.is_pressed():
        if servo_on:
            radio.send("M1")
            servo_on = False
        else:
            radio.send("M2")
            servo_on = True
        msg = None
        while not(msg):
            msg = radio.receive()            
        print(msg)
        time.sleep(DELAY)
    
    elif button_b.is_pressed():
        radio.send("L")
        msg = None
        while not(msg):
            msg = radio.receive()
        print(msg) #send message over serial port to PC
        time.sleep(DELAY)

    


