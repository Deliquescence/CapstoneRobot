import code

import grpc 

import cv2
import numpy as np

import picar_pb2
import picar_pb2_grpc

def requestconnect(stub, name):
	response = stub.ReceiveConnection(picar_pb2.ConnectRequest(message=name))
	print(response.success)	

def switchmode(stub, newmode):
	response = stub.SwitchMode(picar_pb2.ModeRequest(mode = newmode))
	print(response.success)

def setmotion(stub, newthrottle, newdirection):
	response = stub.RemoteControl(picar_pb2.SetMotion(throttle=newthrottle, direction=newdirection))
	
def startstream(stub):
	responses = stub.VideoStream(picar_pb2.StartVideoStream())
	for response in responses:
		frame = response.image
		npimg = np.fromstring(frame, dtype=np.uint8)
		source = cv2.imdecode(npimg, 1)
		cv2.imshow("Stream", source)
		cv2.waitKey(1)
		
		
def stopstream(stub):
	response = stub.StopStream(picar_pb2.EndVideoStream())

def run():
	stub = picar_pb2_grpc.PiCarStub(grpc.insecure_channel('localhost:50051'))
	print('Starting stream')
	startstream(stub)
		
if __name__ == '__main__':
	run()