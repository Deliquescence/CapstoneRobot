import time
import cv2
from tag_detection.detector import estimate_pose


def main():
    camera = cv2.VideoCapture(0)

    try:
        while True:
            start_time = time.time()
            # https://stackoverflow.com/a/48297397
            for _ in range(5):
                camera.grab()
            _, frame = camera.read()
            frame_time = time.time()

            ret = estimate_pose(frame)

            detect_time = time.time()
            print('Got frame in {0} sec and detection ran in {1} sec'
                  .format(frame_time - start_time, detect_time - frame_time))

            if ret is not None:
                rotation = ret[0]
                translation = ret[1]

                print(rotation)
                print(translation)

            else:
                print('Could not detect marker')

            #time.sleep(1)
            s = input('Press q <Enter> to quit or c <Enter> to continue: ')
            if s == 'q':
                break

    finally:
        camera.release()


def from_file():

    fname = "C:/picar/train/tag_orientation_00440.jpg"
    image = cv2.imread(fname)
    print(fname)
    ret = normal_vector(image)

if __name__ == '__main__':
    #from_file()
    main()
