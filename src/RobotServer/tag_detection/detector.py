import cv2
import numpy as np
import math
from .calibrate import get_calibration

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

def isRotationMatrix(R):
    """Checks if a matrix is a valid rotation matrix."""
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype=R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6


def rotationMatrixToEulerAngles(R):
    # https://www.learnopencv.com/rotation-matrix-to-euler-angles/
    assert(isRotationMatrix(R))

    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return np.array([x, y, z])


def estimate_pose(frame):
    """Estimate the position of the tag.
    If tag not found, returns None.
    Otherwise, returns (vector of euler angles, vector of translations), both in order [x, y, z]"""
    TAG_SIZE = 3 # inches

    cam_mtx, dist = get_calibration()

    # setting up our frame
    img = np.array(frame, dtype=np.uint8)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # gather the parameters of the markers
    corners, ids, _reject = cv2.aruco.detectMarkers(
        gray, AR_DICT, parameters=AR_PARAMS, cameraMatrix=cam_mtx, distCoeff=dist)

    if ids is None:
        return None

    rvecs, tvecs, _objPoints = cv2.aruco.estimatePoseSingleMarkers(
        corners, TAG_SIZE, cam_mtx, dist)

    # Rotations:
    # https://stackoverflow.com/questions/13823296/converting-opencv-rotation-and-translation-vectors-to-xyz-rotation-and-xyz-posit
    # https://www.learnopencv.com/rotation-matrix-to-euler-angles/
    # http://answers.opencv.org/question/16796/computing-attituderoll-pitch-yaw-from-solvepnp/?answer=52913#post-id-52913
    # https://docs.opencv.org/2.4/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html#rodrigues
    # http://homepages.inf.ed.ac.uk/rbf/CVonline/LOCAL_COPIES/OWENS/LECT9/node2.html

    # x: We are not really interested in it (and I can't tell the range)
    # y: "lead car is turned right" -> positive, "lead car is turned left" -> negative, "lead car straight" -> ~0
    # z: counterclockwise -, clockwise +, straight vertical ~0

    # Translations:
    # [x, y, z] in tvecs
    # x: right +, left -
    # y: top -, bottom +
    # z: close -, far +

    # TODO: figure out if x and y lines up with tag midpoint or corner

    tx = tvecs[0][0][0]
    ty = tvecs[0][0][1]
    tz = tvecs[0][0][2]

    # print(rvecs)
    # print(tvecs)
    # print(_objPoints)

    rodrigues, _jacobian = cv2.Rodrigues(rvecs)
    # print(rodrigues)

    euler_angles = rotationMatrixToEulerAngles(rodrigues)

    #print(euler_angles)

    rx = euler_angles[0]
    ry = euler_angles[1]
    rz = euler_angles[2]

    return [rx, ry, rz], [tx, ty, tz]
