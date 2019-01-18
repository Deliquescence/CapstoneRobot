import numpy as np
import cv2
import argparse

arDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
parameters = cv2.aruco.DetectorParameters_create()

tLeft = None
tRight = None
bLeft = None
bRight = None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", help="name of the file saved")
    args = vars(ap.parse_args())

    fileName = args["file"]
    filePath = fileName

    camera = cv2.VideoCapture(0)
    
    #loop until 'y' button is pressed and save image with file name
    while(True):
        ret, frame = camera.read()
        
        corners = getCorners(frame)
        if corners is not None:
            tLeft = corners[0][0][0]
            tRight = corners[0][0][1]
            bRight = corners[0][0][2]
            bLeft = corners[0][0][3]

            cv2.rectangle(frame, (tLeft[0],tLeft[1]),(bRight[0], bRight[1]), (0,255,0), 3)

        cv2.imshow('img', frame)
        if cv2.waitKey(1) & 0xFF == ord('y'):
            
            print("Top Left: %f, %f" % (tLeft[0], tLeft[1]))
            print("Top Right: %f, %f" % (tRight[0], tRight[1]))
            print("Bottom Right: %f, %f" % (bRight[0], bRight[1]))
            print("Bottom Left: %f, %f" % (bLeft[0], bLeft[1]))
            cv2.imwrite(filePath, frame)
            cv2.destroyAllWindows()
            break

    camera.release()


def getCorners(img):
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #gather the parameters of the markers ID is important to us
    corners, ids, reject = cv2.aruco.detectMarkers(grayImg, arDict, parameters=parameters)
    if ids is not None:
        return corners

if __name__ == "__main__":
    main()