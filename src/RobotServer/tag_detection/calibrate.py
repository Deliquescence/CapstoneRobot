import cv2
import numpy as np


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

        print('Press q to quit or any other key continue.')
        key = cv2.waitKey(0) & 0xFF
        if key == ord('q'):
            break

    camera.release()
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(object_points, image_points, gray.shape[::-1], None, None)

    if ret:
        print('Calibration complete.')
        print('mtx = {0}'.format(mtx))
        print('dist = {0}'.format(dist))
        return mtx, dist
    else:
        print('Could not calibrate.')
        return None


def save_calibration(file_name, mtx, dist):
    """Saves the given calibration to a file at the given path."""
    np.savez(file_name, mtx=mtx, dist=dist)


def load_calibration(file_name):
    """Returns the calibration saved in the file at the given path."""
    files = np.load(file_name).files
    return files['mtx'], files['dist']


def main():
    calibration = calibrate()
    if calibration is not None:
        save_calibration(*calibration)


if __name__ == '__main__':
    main()
