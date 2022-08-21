#second microbit acting as radio adapter to pass from radio over serial

from microbit import button_a, button_b, uart, display
import radio
import time

START_GROUP = 2
CHANNEL = 17
radio.config(group=START_GROUP,queue=1,channel=CHANNEL,length=100) #group = channel; queue=1 ensures that the microbits only store a backlog of 1 message rather than storing loads, meaning they can't get clogged up. The microbits are always listening even when doing something else and messages are added to a queue. Here we cap the queue at size 1 message
radio.on() #radio communication is off by default to save power so we need to activate it.
DELAY = 1

servo_on = False
uart.init(baudrate=115200)

while True:
    msgBytes = uart.read()
    if msgBytes:
        display.scroll("Received serial")
        radio.send_bytes(msgBytes)
        response = None
        while response == None:
            response = radio.receive_bytes()
        #print(response)
        uart.write(response) #send out over serial
    
