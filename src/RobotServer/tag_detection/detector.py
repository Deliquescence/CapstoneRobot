import cv2
import numpy as np

AR_DICT = cv2.aruco.Dictionary_create(1, 3)
AR_PARAMS = cv2.aruco.DetectorParameters_create()


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
