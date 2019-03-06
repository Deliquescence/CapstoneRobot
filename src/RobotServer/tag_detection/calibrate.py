import cv2
import numpy as np

DEFAULT_FILE_NAME = "calibration.npz"

# Saved/cached calibration values. See `get_calibration`.
_matrix = None
_distortion = None


def calibrate():
    """Interactively finds a calibration for the camera by taking images from the camera
    that contain an image of an 8x8 chessboard. Returns a tuple of the camera matrix
    and distance coefficients encoding the specific qualities/optics of the camera
    or None if calibration fails. Can be used to determine the orientation and distance
    of an aruco marker."""
    camera = cv2.VideoCapture(0)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    prepared_object_points = np.zeros((7*7, 3), np.float32)
    prepared_object_points[:, :2] = np.mgrid[0:7, 0:7].T.reshape(-1, 2)

    object_points = []
    image_points = []
    count = 0

    while True:
        _, img = camera.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (7, 7), None)

        if ret:
            print('Found chessboard corners.')
            count += 1
            print('Found {0} images with chessboard corners so far.'.format(count))

            object_points.append(prepared_object_points)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            image_points.append(corners2)
        else:
            print('Did not find chessboard corners.')

        s = input('Press q <Enter> to quit or c <Enter> to continue: ')
        if s == 'q':
            break

    camera.release()
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(object_points, image_points, gray.shape[::-1], None, None)

    if ret:
        print('Calibration complete.')
        print('mtx = {0}'.format(mtx))
        print('dist = {0}'.format(dist))
        _matrix = mtx
        _distortion = dist
        return mtx, dist
    else:
        print('Could not calibrate.')
        return None


def save_calibration(mtx, dist, file_name=DEFAULT_FILE_NAME):
    """Saves the given calibration to a file at the given path."""
    np.savez(file_name, mtx=mtx, dist=dist)


def load_calibration(file_name=DEFAULT_FILE_NAME):
    """Returns the calibration saved in the file at the given path."""
    files = np.load(file_name).files
    return files['mtx'], files['dist']


def get_calibration(file_name=DEFAULT_FILE_NAME):
    """Returns the cached calibration, or loads it from the file if necessary."""
    global _matrix, _distortion

    if _matrix is None or _distortion is None:
        _matrix, _distortion = load_calibration(file_name)

    return _matrix, _distortion


def main():
    calibration = calibrate()
    if calibration is not None:
        save_calibration(*calibration)


if __name__ == '__main__':
    main()
