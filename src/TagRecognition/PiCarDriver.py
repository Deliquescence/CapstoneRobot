from picar import front_wheels
import picar
import cv2
from concurrent import futures
import time
import picarserver
import picarhelper
import socket
import grpc
import picar_pb2
import picar_pb2_grpc


picar.setup()
rear_wheels_enabled = True
front_wheels_enabled = True

FW_ANGLE_MAX = 90+30
FW_ANGLE_MIN = 90-30

fw = front_wheels.Front_Wheels()
fw_default = picarhelper.getDefaultAngle(socket.gethostname())

FW_ANGLE_MAX = fw_default+30
FW_ANGLE_MIN = fw_default-30


#fw.offset = 0
#fw.turn(fw_default)

mode = 0


#det up our tag dictionary and parameter value 
#we use tag ids 0-3
arDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
parameters = cv2.aruco.DetectorParameters_create()




#get a reference to the camera, default is 0
camera = cv2.VideoCapture(0)
frame = None
roiPts = []
inputMode = False

def main():

    #start the server

    server = picarserver.getServer()
    server.start()

    print "Server Started on "+socket.gethostname()+"\n"
    print "Press Ctrl-C to quit"

    move(0.0,0.0)

    # loop unless break occurs
    while True:

        #check if key pressed

        k = cv2.waitKey(1) & 0xFF

        #if q key is pressed we break loop
        if k == ord('q'):
            break

        # get reference to current mode
        mode = picarserver.mode

        if mode == 1:
            # leader mode
            #print "picar set to LEADER"
            move(picarserver.throttle, picarserver.direction)

        elif mode == 2:
            # follower mode
            #print "picar set to FOLLOWER"
            throttle, direction = tagID()
            move(throttle, direction)
             
        # else:
            # idle mode
            #print "picar set to IDLE"
        
        #wait 1 second after loop    
        time.sleep(1/60)

    #cleanup    
    destroy()

def move(throttle, direction):
    motor_speed = int(abs(throttle)*100)
    fw_angle = fw_default+(30*(direction))


    if front_wheels_enabled and (fw_angle >= FW_ANGLE_MIN and fw_angle <= FW_ANGLE_MAX):
        fw.turn(fw_angle)
    if rear_wheels_enabled:
        if (throttle > 0.0):
            picarhelper.move_forward(motor_speed)
        elif (throttle < 0.0):
            picarhelper.move_backward(motor_speed)
        else:
            picarhelper.stop()


#method to recognize tags
def tagID():
    ret, frame = camera.read()
#setting up our frame
    theGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('frame', theGray)
    
#gather the parameters of the markers  ID is important to us    
    corners, ids, reject = cv2.aruco.detectMarkers(theGray, arDict, parameters=parameters)
    
    #Calculating the angle we need to turn the car
    #uses a system similar to permission setting to add together ids to see what direction should be turned
    if ids is not None:
         
         idCounter = 0
         idSize = len(ids)
         for i in range(idSize):
             for j in range(9):
                 if (j == ids[i]):
                     idCounter = idCounter + ids[i]    
         if (idCounter == 1 or idCounter == 3 or idCounter ==7):
            return(1, 60) #("left")
         elif (idCounter == 8 or idCounter == 12 or idCounter == 14):
            return(1, 120) #("right")
         elif (idCounter == 6):
            return(1, 90) #("straight")
         elif (idCounter == 2):
            return(1, 105) #("slight right")
         elif (idCounter == 4):
            return(1, 75) #("slight left")
    else:
        return(0, 90)
    



def destroy():
    picarhelper.stop()
    camera.release()
    cv2.destroyAllWindows()

def test():
    print "Begin Test!"

    move(0.0,0.0)
    time.sleep(1)
    move(0.0, 1.0)
    time.sleep(1)
    move(0.0, -1.0)
    time.sleep(1)
    move(0.0,0.0)
    print "End Test!"
    destroy()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt():
        destroy()