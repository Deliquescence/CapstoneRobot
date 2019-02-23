import cv2
import numpy as np
import pandas as pd
import os
from PIL import Image

import tag_detector
from states import State
from actions import Action


BASE_PATH = "../../../../train_data"
IMAGE_DIR = "train"
IN_CSV = "labels.csv"  # For the action done
OUT_CSV = "rl_Labels.csv"

# Training data is 320x240 but pi camera is 640x480
tag_detector.NEAR_THRESHOLD /= 2
tag_detector.FAR_THRESHOLD /= 2


STOP_THRESHOLD = 0.01
LOW_THRESHOLD = 0.4

STRAIGHT_THRESHOLD = 0.1
SOFT_THRESHOLD = 0.5


def map_action(throttle, direction):
    """Return the action representing the given throttle and direction."""

    if throttle < -1*LOW_THRESHOLD:
        actions = [Action.rev_high_hard_left, Action.rev_high_soft_left,
                   Action.rev_high_straight, Action.rev_high_soft_right, Action.rev_high_hard_right]

    elif throttle < -1*STOP_THRESHOLD:
        actions = [Action.rev_low_hard_left, Action.rev_low_soft_left,
                   Action.rev_low_straight, Action.rev_low_soft_right, Action.rev_low_hard_right]

    elif throttle <= STOP_THRESHOLD:
        actions = [Action.stop]*5

    elif throttle <= LOW_THRESHOLD:
        actions = [Action.low_hard_left, Action.low_soft_left,
                   Action.low_straight, Action.low_soft_right, Action.low_hard_right]

    else:
        actions = [Action.high_hard_left, Action.high_soft_left,
                   Action.high_straight, Action.high_soft_right, Action.high_hard_right]

    if direction < -1*SOFT_THRESHOLD:
        return actions[0]
    elif direction < -1*STRAIGHT_THRESHOLD:
        return actions[1]
    elif direction <= STRAIGHT_THRESHOLD:
        return actions[2]
    elif direction <= SOFT_THRESHOLD:
        return actions[3]
    else:
        return actions[4]


def reward(tag_loc, action):
    if tag_loc is None:
        return 0.0

    edge_len = tag_loc.avg_edge_len
    # todo? squared distance error. Would need fn for tag_length -> distance.
    if edge_len < tag_detector.NEAR_THRESHOLD and edge_len > tag_detector.FAR_THRESHOLD:
        return 1.0
    else:
        return -1.0

    return 0.0


def main():
    os.chdir(BASE_PATH)

    df = pd.DataFrame(columns=['file_name', 'state', 'tag_loc'])

    for file_name in os.listdir(IMAGE_DIR):
        file_name_with_folder = "{0}/{1}".format(IMAGE_DIR, file_name)
        img = Image.open(file_name_with_folder)
        img = np.array(img)

        loc = tag_detector.tag_loc(img)
        state = tag_detector.state_from_loc(loc)

        logging = False
        if logging:
            print(file_name)
            if loc is not None:
                print(loc.x_pos, loc.avg_edge_len)
                print(state)

        # state = tag_detector.state_from_frame(img)

        df = df.append(
            {"file_name": file_name_with_folder, "state": state, "tag_loc": loc}, ignore_index=True)

    print(df['state'].value_counts())

    df = df.merge(
        pd.read_csv(IN_CSV), left_on="file_name", right_on="image_file", how="inner")

    df['action'] = df.apply(lambda row: map_action(
        row['throttle'], row['direction']), axis=1)

    df['reward'] = df.apply(lambda row: reward(
        row['tag_loc'], row['action']), axis=1)

    rl_labels = df[['state', 'action', 'reward']]
    print(rl_labels)
    rl_labels.to_csv(OUT_CSV, index=False)


if __name__ == '__main__':
    main()
