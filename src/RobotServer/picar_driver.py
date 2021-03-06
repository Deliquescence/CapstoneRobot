import picar
import cv2
import time
from server import picar_server
import picar_helper
from queue import Queue
import socket
import numpy as np
from follower import Follower

picar.setup()

# det up our tag dictionary and parameter value
# we use tag ids 1,2,4,8

# Error with dependencies,
#  cv2.cv2 has no attirbute 'aruco'
# but with ML follower we don't need this, so remove for now
#arDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
#parameters = cv2.aruco.DetectorParameters_create()

# get a reference to the camera, default is 0
camera = cv2.VideoCapture(0)


def default_follower():
    try:
        return Follower.load(epsilon=0.0)
    except IOError:  # file does not exist
        print("Failed to load follower file")
        return Follower()


def main(start_mode=0):
    driver = PiCarDriver(default_follower())

    try:
        # start the server
        server = picar_server.getServer(driver)
        server.start()

        print('Server Started on' + socket.gethostname() + '\n')
        print('Press Ctrl-C to quit')

        # start the driver
        driver.run(start_mode=start_mode)
    finally:
        driver.follower.save()  # Save follower when done
        destroy()


class PiCarDriver(object):
    def __init__(self, follower):
        self.mode = 0
        self.follower = follower
        self.next_throttle_and_dir = (0.0, 0.0)  # Assigned by server. Used by main() to move picar
        self._streaming = False
        self.stream_queue = Queue(maxsize=20)
        self._prev_throttle = 0.0  # Assigned when moved. Pushed to stream
        self._prev_direction = 0.0  # Assigned when moved. Pushed to stream

    def set_mode(self, mode):
        """Called from server to set mode (follower/driver)"""
        self.mode = mode
        if mode == 0:
            self.follower.reset_state()

    def set_model(self, model: int):
        """Sets model used in follower mode. Called from server.
        Returns a bool indicating whether the supplied model version is a valid version."""
        if model == 0:
            self.follower = default_follower()

        elif model == 1:
            import legacy_follower_pid
            self.follower = legacy_follower_pid.Follower()

        else:
            return False

        return True

    def set_throttle_and_dir(self, throttle, direction):
        """Called from server to operate in driving mode."""
        self.next_throttle_and_dir = (throttle, direction)

    def start_streaming(self):
        """Called from server to start streaming."""
        self.stream_queue = Queue(maxsize=20)
        self._streaming = True

    def stop_streaming(self):
        """Called from server to stop streaming."""
        self._streaming = False
        self.stream_queue = Queue(maxsize=20)

    def is_streaming(self):
        """Queried from within this class and from server to
        determine if we are streaming."""
        return self._streaming

    def run(self, start_mode=0):
        self._move(0.0, 0.0)

        # loop unless break occurs
        while True:
            # get the current frame
            _, frame = camera.read()

            if self.mode == 1:
                # leader mode
                self._move(self.next_throttle_and_dir[0],
                           self.next_throttle_and_dir[1])
            elif self.mode == 2:
                # follower mode
                # if no base corners, get corners
                throttle, direction = self.follower.get_action(frame)
                self._move(throttle, direction)
            else:
                self._move(0.0, 0.0)

            # Add frame and move vector to stream queue
            if self.is_streaming():
                self.stream_queue.put(
                    StreamData(frame, self._prev_throttle,
                               self._prev_direction))

            time.sleep(1 / 30)

    def _move(self, throttle, direction):
        """Sets throttle and direction for picar. Additionally communicates this information
        with the attached server. Call this from this class."""
        self._prev_throttle = throttle
        self._prev_direction = direction
        picar_helper.move(throttle, direction)


class StreamData(object):
    def __init__(self, frame, throttle, direction):
        self.frame = frame
        self.throttle = throttle
        self.direction = direction


class BaseCorners(object):
    pass


# method to recognize tags
def tagID(frame, bc):
    # setting up our frame
    img = np.array(frame, dtype=np.uint8)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # gather the parameters of the markers  ID is important to us
    corners, ids, reject = cv2.aruco.detectMarkers(gray, arDict,
                                                   parameters=parameters)

    if ids is not None:
        # CORNER LAYOUT: corner[0][corner][x][y]
        # starts top left and moves clockwise
        tLeft = corners[0][0][0]
        tRight = corners[0][0][1]
        bRight = corners[0][0][2]
        bLeft = corners[0][0][3]

        # draw rectangle around detected tag and baseline
        cv2.rectangle(frame, (bc.baseTopLeft[0], bc.baseTopLeft[1]),
                      (bc.baseBottomRight[0], bc.baseBottomRight[1]),
                      (0, 255, 0),
                      2)
        cv2.rectangle(frame, (tLeft[0], tLeft[1]), (bRight[0], bRight[1]),
                      (0, 0, 255), 2)

        # insert rest of follower code here
        topEdge = (tRight[0] - tLeft[0], tRight[1] - tLeft[1])
        rightEdge = (bRight[0] - tRight[0], bRight[1] - tRight[1])
        bottomEdge = (bRight[0] - bLeft[0], bRight[1] - bLeft[1])
        leftEdge = (bLeft[0] - tLeft[0], bLeft[1] - tLeft[1])
        avgEdge = (topEdge[0] + rightEdge[1] + bottomEdge[0] + leftEdge[1]) / 4

        # calculate speed from avg edge comparison
        speedVar = 1.0 - (avgEdge / bc.baseAvgEdge)

        tagMidX = (topEdge[0] / 2) + bLeft[0]
        tagMidY = (rightEdge[1] / 2) + tRight[1]
        tagMidPoint = (tagMidX, tagMidY)

        # calculates what fraction of total displacement occurs in X direction,
        # should be number between -1.0 and 1.0
        tagXDisplacement = tagMidPoint[0] - bc.baseMidPoint[0]
        tagDisplacementAmt = tagXDisplacement / bc.maxTagDisplacement
        tagThreshold = 10

        if avgEdge < bc.baseAvgEdge - tagThreshold:
            # too far from leader, move closer
            return speedVar, tagDisplacementAmt
        elif avgEdge > bc.baseAvgEdge + tagThreshold:
            # too close to leader, move away
            return -0.3, -tagDisplacementAmt
        else:
            return 0.0, 0.0
    else:
        return 0.0, 0.0


def getBaseCorners(frame):
    grayImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, reject = cv2.aruco.detectMarkers(grayImg, arDict,
                                                   parameters=parameters)
    if ids is not None:
        if corners is not None:
            bc = BaseCorners()
            bc.baseTopLeft = corners[0][0][0]
            bc.baseTopRight = corners[0][0][1]
            bc.baseBottomRight = corners[0][0][2]
            bc.baseBottomLeft = corners[0][0][3]

            bc.baseTopEdge = (
                bc.baseTopRight[0] - bc.baseTopLeft[0],
                bc.baseTopRight[1] - bc.baseTopLeft[1])
            bc.baseRightEdge = (bc.baseBottomRight[0] - bc.baseTopRight[0],
                                bc.baseBottomRight[1] - bc.baseTopRight[1])
            bc.baseBottomEdge = (bc.baseBottomRight[0] - bc.baseBottomLeft[0],
                                 bc.baseBottomRight[1] - bc.baseBottomLeft[1])
            bc.baseLeftEdge = (
                bc.baseBottomLeft[0] - bc.baseTopLeft[0],
                bc.baseBottomLeft[1] - bc.baseTopLeft[1])
            bc.baseAvgEdge = (bc.baseTopEdge[0] + bc.baseRightEdge[1] +
                              bc.baseBottomEdge[0] +
                              bc.baseLeftEdge[1]) / 4

            bc.baseMidX = (bc.baseTopEdge[0] / 2) + bc.baseTopLeft[0]
            bc.baseMidY = (bc.baseRightEdge[1] / 2) + bc.baseTopRight[1]
            bc.baseMidPoint = (bc.baseMidX, bc.baseMidY)
            bc.maxTagDisplacement = bc.baseMidPoint[0] - (bc.baseTopEdge[0] / 2)

            return bc

    return None


def destroy():
    picar_helper.stop()
    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
