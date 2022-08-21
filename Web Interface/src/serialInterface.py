#device manager - ports, com and LPT, usb serial device

# do the protobuf stuff in here. Simple forwardin the other one.


import serial

class SerialContact:
    
    def __init__(self) ->None:
        return

    def __enter__(self) -> None:    
        self.ser = serial.Serial()
        self.ser.baudrate = 115200
        self.ser.port = "COM5"
        self.ser.open()

        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:    
        self.ser.close()
    

    def makeRequest(self,requestBytes,responseBytesExpected):
        self.ser.write(requestBytes)
        microbitdata = self.ser.read(responseBytesExpected)
        print(microbitdata)
        return microbitdata
