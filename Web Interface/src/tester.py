import drone_pb2
import serialInterface

myReq = drone_pb2.Request()
myReq.requesttype = 2
myser = serialInterface.SerialContact()

result = myser.makeRequest(myReq.SerializeToString(),4) #or 18

myResponse = protobuftemp.LocationResponse()
myResponse.ParseFromString(result)
print(myResponse.lat)
print(myResponse.lon)
