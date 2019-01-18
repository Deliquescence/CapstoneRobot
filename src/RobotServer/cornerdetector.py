import cv2
import argparse

arDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
parameters = cv2.aruco.DetectorParameters_create()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", help="name of the file input")
    args = vars(ap.parse_args())

    fileName = args["file"]

    img = cv2.imread(fileName, 0)

    corners = getCorners(img)
    
    if corners is not None:
        tLeft = corners[0][0][0]
        tRight = corners[0][0][1]
        bRight = corners[0][0][2]
        bLeft = corners[0][0][3]
        print("What")
        print "Top Left: {}, {}".format(tLeft[0], tLeft[1])
        print "Top Right: {}, {}".format(tRight[0], tRight[1])
        print "Bottom Right: {}, {}".format(bRight[0], bRight[1])
        print "Bottom Left: {}, {}".format(bLeft[0], bLeft[1])
        
        cv2.imshow("image", img)
        cv2.waitKey(0)
        cv2.detroyAllWindows()
    else:
        print ("No corners detected!")

def getCorners(img):
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #gather the parameters of the markers ID is important to us
    corners, ids, reject = cv2.aruco.detectMarkers(grayImg, arDict, parameters=parameters)
    if ids is not None:
        return corners