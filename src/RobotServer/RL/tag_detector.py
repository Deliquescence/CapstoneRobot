import cv2
import numpy as np
import time

from .states import State

AR_DICT = cv2.aruco.Dictionary_create(1, 3)
AR_PARAMS = cv2.aruco.DetectorParameters_create()

LEFT_THRESHOLD = -50
RIGHT_THRESHOLD = 50
# These were chosen based on 640 width image
NEAR_THRESHOLD = 125 / 640
FAR_THRESHOLD = 70 / 640


def state_from_frame(frame):
    """Returns a State indicating the approximate location of the tag in the given frame."""
    return state_from_loc(tag_loc(frame))


def state_from_loc(loc):
    """Returns a State indicating the approximate location of the tag in the given PreciseLocation."""

    if loc is None:
        return State.unknown
    else:
        # Select direction
        if loc.x_pos <= LEFT_THRESHOLD:
            states = [State.far_left, State.good_left, State.near_left]
        elif loc.x_pos >= RIGHT_THRESHOLD:
            states = [State.far_right, State.good_right, State.near_right]
        else:
            states = [State.far_straight, State.good_straight, State.near_straight]

        # Select distance
        if loc.avg_edge_len >= NEAR_THRESHOLD:
            return states[2]
        elif loc.avg_edge_len <= FAR_THRESHOLD:
            return states[0]
        else:
            return states[1]


class PreciseLocation(object):
    """Represents a precise location of a tag within an image.

    avg_edge_len is the average length of the edges of the marker in pixels.
    x_pos is the x coordinate in pixels relative to the center of the image.
    Both are floats."""

    def __init__(self, avg_edge_len, x_pos):
        self.avg_edge_len = avg_edge_len
        self.x_pos = x_pos


def tag_loc(frame):
    """Returns the PreciseLocation of the tag in the frame. Returns None when the tag is not detected."""

    # setting up our frame
    img = np.array(frame, dtype=np.uint8)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # gather the parameters of the markers  ID is important to us
    corners, ids, reject = cv2.aruco.detectMarkers(gray, AR_DICT, parameters=AR_PARAMS)

    if ids is not None:
        # starts top left and moves clockwise
        t_left = corners[0][0][0]
        t_right = corners[0][0][1]
        b_right = corners[0][0][2]
        b_left = corners[0][0][3]

        # insert rest of follower code here
        top_edge = (t_right[0] - t_left[0], t_right[1] - t_left[1])
        right_edge = (b_right[0] - t_right[0], b_right[1] - t_right[1])
        bottom_edge = (b_right[0] - b_left[0], b_right[1] - b_left[1])
        left_edge = (b_left[0] - t_left[0], b_left[1] - t_left[1])
        avg_edge = (top_edge[0] + right_edge[1] + bottom_edge[0] + left_edge[1]) / 4

        _height, width = frame.shape[:2]
        tag_mid_x = (top_edge[0] / 2) + b_left[0] - width / 2

        return PreciseLocation(avg_edge / width, tag_mid_x)
    else:
        return None


def main():
    camera = cv2.VideoCapture(0)

    try:
        while True:
            start_time = time.time()
            _, frame = camera.read()
            frame_time = time.time()
            loc = tag_loc(frame)
            detect_time = time.time()
            print('Got frame in {0} sec and marker detection ran in {1} sec'
                  .format(frame_time - start_time, detect_time - frame_time))
            if loc is not None:
                print(
                    'Average edge length of marker in pixels is {0}'
                    ' and x pos of tag center relative to image center is {1}'
                        .format(loc.avg_edge_len, loc.x_pos))
                state = state_from_loc(loc)
                print('And computed state is {0}'.format(state))
            else:
                print('Could not detect marker')
            time.sleep(1)
    finally:
        camera.release()


if __name__ == '__main__':
    main()
