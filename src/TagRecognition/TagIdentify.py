import numpy as np
import cv2


#getting the dictionary of the markers
#our ids are 1,2,4,8
arDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
parameters = cv2.aruco.DetectorParameters_create()

#where we define car camera;  this is for testing and needs to be updated for true implementation
camera = cv2.VideoCapture(0)



        




while(True):
    
    ret, frame = camera.read()
#setting up our frame
    theGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', theGray)
#gather the parameters of the markers  get size of id    
    corners, ids, reject = cv2.aruco.detectMarkers(theGray, arDict, parameters=parameters)
    
    
    
    #Calculating the angle we need to turn the car
    if ids is not None:
         print(3)
         idCounter = 0
         idSize = len(ids)
         for i in range(idSize):
             for j in range(9):
                 if (j == ids[i]):
                     idCounter = idCounter + ids[i]    
         if (idCounter == 1 or idCounter == 3 or idCounter ==7):
            print(60) #("left")
         elif (idCounter == 8 or idCounter == 12 or idCounter == 14):
            print(120) #("right")
         elif (idCounter == 6):
            print(90) #("straight")
         elif (idCounter == 2):
            print(105) #("slight right")
         elif (idCounter == 4):
            print(75) #("slight left")
    
                
    
    
   
   

    # Display the frame for our testing
    cv2.imshow('frame',theGray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


camera.release()
cv2.destroyAllWindows()

