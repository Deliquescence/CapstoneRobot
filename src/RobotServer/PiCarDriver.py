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
import numpy as np

picar.setup()
rear_wheels_enabled = True
front_wheels_enabled = True

fw = front_wheels.Front_Wheels()
fw_default = picarhelper.getDefaultAngle(socket.gethostname())

FW_ANGLE_MAX = fw_default+30
FW_ANGLE_MIN = fw_default-30

mode = 0

baseTopLeft = None
baseTopRight = None
baseBottomRight = None
baseBottomLeft = None

baseTopEdge = None
baseRightEdge = None
baseBottomEdge = None
baseLeftEdge = None
baseAvgEdge = None

baseMidX = None
baseMidY = None
baseMidPoint = None

maxTagDisplacement = None
hasBaseCorners = False

#det up our tag dictionary and parameter value 
#we use tag ids 1,2,4,8
arDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
parameters = cv2.aruco.DetectorParameters_create()


#get a reference to the camera, default is 0
camera = cv2.VideoCapture(0)
frame = None

def main():
    global baseTopLeft, baseTopRight, baseBottomRight, baseBottomLeft
    global baseTopEdge, baseRightEdge, baseBottomEdge, baseLeftEdge, baseAvgEdge
    global baseMidX, baseMidY, baseMidPoint
    global maxTagDisplacement, frame, hasBaseCorners

    #start the server
    server = picarserver.getServer()
    server.start()

    print "Server Started on "+socket.gethostname()+"\n"
    print "Press Ctrl-C to quit"

    picarhelper.move(0.0,0.0)

    # loop unless break occurs
    while True:

        #check if key pressed
        k = cv2.waitKey(1) & 0xFF

        #if q key is pressed we break loop
        if k == ord('q'):
            break

        # get reference to current mode
        mode = picarserver.mode
        #get the current frame
        (grabbed, frame) = camera.read()

        if mode == 1:
            # leader mode
            #print "picar set to LEADER"
            picarhelper.move((picarserver.throttle/2), picarserver.direction)
        elif mode == 2:
            # follower mode
            #if no base corners, get corners
            if not hasBaseCorners:
                getBaseCorners()
            #if we have base corners, now enter follower
            if hasBaseCorners:
                throttle, direction = tagID()
                picarhelper.move(throttle, direction)
            else:
                print "Base Tag Corners Not Detected!"
        else:
            picarhelper.move(0.0, 0.0)
            baseTopLeft = None
            baseTopRight = None
            baseBottomRight = None
            baseBottomLeft = None

            baseTopEdge = None
            baseRightEdge = None
            baseBottomEdge = None
            baseLeftEdge = None
            baseAvgEdge = None

            baseMidX = None
            baseMidY = None
            baseMidPoint = None

            maxTagDisplacement = None
            hasBaseCorners = False


        #set frame to send to desktop
        picarserver.setFrame(frame)
        time.sleep(1/30)

    #cleanup
    destroy()


#method to recognize tags
def tagID():
    #setting up our frame
    global frame
    img = np.array(frame, dtype=np.uint8)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #gather the parameters of the markers  ID is important to us    
    corners, ids, reject = cv2.aruco.detectMarkers(gray, arDict, parameters=parameters)
    

    if ids is not None:
        #CORNER LAYOUT: corner[0][corner][x][y]
        #starts top left and moves clockwise
        tLeft = corners[0][0][0]
        tRight = corners[0][0][1]
        bRight = corners[0][0][2]
        bLeft = corners[0][0][3]

        #draw rectangle around detected tag and baseline 
        cv2.rectangle(frame, (baseTopLeft[0],baseTopLeft[1]),(baseBottomRight[0],baseBottomRight[1]), (0,255,0), 2)
        cv2.rectangle(frame, (tLeft[0],tLeft[1]),(bRight[0], bRight[1]), (0,0,255), 2)
        
        #insert rest of follower code here
        topEdge = (tRight[0]-tLeft[0], tRight[1]-tLeft[1])
        rightEdge = (bRight[0]-tRight[0], bRight[1]-tRight[1])
        bottomEdge = (bRight[0]-bLeft[0], bRight[1]-bLeft[1])
        leftEdge = (bLeft[0]- tLeft[0], bLeft[1]-tLeft[1])
        avgEdge = (topEdge[0] + rightEdge[1] + bottomEdge[0] + leftEdge[1])/4
        
        # calculate speed from avg edge comparison
        speedVar = 1.0 - (avgEdge/baseAvgEdge)

        tagMidX = (topEdge[0]/2)+bLeft[0]
        tagMidY = (rightEdge[1]/2)+tRight[1]
        tagMidPoint = (tagMidX, tagMidY)
        
        # calculates what fraction of total displacement occurs in X direction, should be number between -1.0 and 1.0
        tagXDisplacement = tagMidPoint[0] - baseMidPoint[0]
        tagDisplacementAmt = tagXDisplacement/maxTagDisplacement
        tagThreshold = 10

        if (avgEdge < baseAvgEdge-tagThreshold):
            #too far from leader, move closer
            return(speedVar, tagDisplacementAmt)
        elif (avgEdge > baseAvgEdge+tagThreshold):
            #too close to leader, move away
            return(-0.3, -tagDisplacementAmt)
        else:
            return (0.0, 0.0)
    else:
        return(0.0, 0.0)

def getBaseCorners():
    global baseTopLeft, baseTopRight, baseBottomRight, baseBottomLeft
    global baseTopEdge, baseRightEdge, baseBottomEdge, baseLeftEdge, baseAvgEdge
    global baseMidX, baseMidY, baseMidPoint
    global maxTagDisplacement, frame, hasBaseCorners

    grayImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, reject = cv2.aruco.detectMarkers(grayImg, arDict, parameters=parameters)
    if ids is not None:
        if corners is not None:
            baseTopLeft = corners[0][0][0]
            baseTopRight = corners[0][0][1]
            baseBottomRight = corners[0][0][2]
            baseBottomLeft = corners[0][0][3]

            baseTopEdge = (baseTopRight[0]-baseTopLeft[0], baseTopRight[1]-baseTopLeft[1])
            baseRightEdge = (baseBottomRight[0]-baseTopRight[0], baseBottomRight[1]-baseTopRight[1])
            baseBottomEdge = (baseBottomRight[0]-baseBottomLeft[0], baseBottomRight[1]-baseBottomLeft[1])
            baseLeftEdge = (baseBottomLeft[0]-baseTopLeft[0], baseBottomLeft[1]-baseTopLeft[1])
            baseAvgEdge = (baseTopEdge[0]+baseRightEdge[1]+baseBottomEdge[0]+baseLeftEdge[1])/4

            baseMidX = (baseTopEdge[0]/2)+baseTopLeft[0]
            baseMidY = (baseRightEdge[1]/2)+baseTopRight[1]
            baseMidPoint = (baseMidX, baseMidY)
            maxTagDisplacement = baseMidPoint[0]-(baseTopEdge[0]/2)
            hasBaseCorners = True




def destroy():
    picarhelper.stop()
    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt():
        destroy()
