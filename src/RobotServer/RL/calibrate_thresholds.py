import cv2
import time

from ..tag_detection.detector import tag_loc
from .states import state_from_loc


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
