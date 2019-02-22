import cv2
import numpy as np
import pandas as pd
import os
from PIL import Image

import tag_detector
from states import State


BASE_PATH = "../../../../train_data"
IMAGE_DIR = "train"
IN_CSV = "labels.csv"  # For the action done
OUT_CSV = "rl_Labels.csv"

# Training data is 320x240 but pi camera is 640x480
tag_detector.NEAR_THRESHOLD /= 2
tag_detector.FAR_THRESHOLD /= 2

def main():
    os.chdir(BASE_PATH)

    classifications = pd.DataFrame(columns=['file_name', 'state'])

    for file_name in os.listdir(IMAGE_DIR):
        print(file_name)
        img = Image.open("{0}/{1}".format(IMAGE_DIR, file_name))
        img = np.array(img)

        loc = tag_detector.tag_loc(img)
        state = tag_detector.state_from_loc(loc)

        if loc is not None:
            print(loc.x_pos, loc.avg_edge_len)
            print(state)

        # state = tag_detector.state_from_frame(img)

        classifications = classifications.append(
            {"file_name": file_name, "state": state}, ignore_index=True)

    print(classifications)
    print(classifications['state'].value_counts())
    classifications.to_csv(OUT_CSV, index=False)


if __name__ == '__main__':
    main()
