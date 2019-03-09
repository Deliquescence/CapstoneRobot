import time
import cv2
from tag_detection.detector import estimate_pose, process_color


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

            pose = estimate_pose(frame)
            pose_time = time.time()

            pct_pixels = process_color(frame)
            color_time = time.time()

            print('Timings: frame={0} sec\t pose={1} sec\t color={2} sec'
                  .format(frame_time - start_time, pose_time - frame_time, color_time - pose_time))

            if pose is not None:
                rotation = pose[0]
                translation = pose[1]

                print('Pose data:')
                print(rotation)
                print(translation)

            else:
                print('Could not detect marker')

            print('Color data {}:'.format(pct_pixels))

            #time.sleep(1)
            s = input('Press q <Enter> to quit or c <Enter> to continue: ')
            if s == 'q':
                break

    finally:
        camera.release()


def from_file():

    fnames = []
    for fname in fnames:
        image = cv2.imread(fname)
        print(fname)
        print(process_color(image))
        #pose = estimate_pose(image)

if __name__ == '__main__':
    #from_file()
    main()
