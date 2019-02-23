import cv2
import numpy as np
import pandas as pd
import os
from PIL import Image

import tag_detector
from states import State
import actions
from actions import Action


BASE_PATH = "../../../../train_data"
IMAGE_DIR = "train"
IN_CSV = "labels.csv"  # For the action done
OUT_CSV = "rl_Labels.csv"

# Training data is 320x240 but pi camera is 640x480
tag_detector.NEAR_THRESHOLD /= 2
tag_detector.FAR_THRESHOLD /= 2


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


def next_state(df, row):
    # print("next_state")
    # print(df_row)
    try:
        next_row = df.iloc[row.name + 1]
    except IndexError:
        return State.unknown

    current_name_splits = row['file_name'].split('_')
    next_name_splits = next_row['file_name'].split('_')
    if next_name_splits[0] != current_name_splits[0]:
        # Not same training label
        return State.unknown

    current_num = current_name_splits[1].split(".")[0]
    next_num = next_name_splits[1].split(".")[0]
    if int(next_num) != int(current_num) + 1:
        # Not consecutive
        return State.unknown

    return next_row['state']


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

    df['action'] = df.apply(lambda row: actions.from_throttle_direction(
        row['throttle'], row['direction']), axis=1)

    df['reward'] = df.apply(lambda row: reward(
        row['tag_loc'], row['action']), axis=1)

    df['next_state'] = df.apply(lambda row: next_state(df, row), axis=1)

    rl_labels = df[['state', 'action', 'reward', 'next_state']]

    print(rl_labels)
    # change enum to ints
    # pandas is yelling at me about view vs copy but this seems to do what I want
    rl_labels['next_state'] = df.apply(
        lambda row: row['next_state'].value, axis=1)
    rl_labels['state'] = df.apply(
        lambda row: row['state'].value, axis=1)
    rl_labels['action'] = df.apply(
        lambda row: row['action'].value, axis=1)

    print(rl_labels)
    rl_labels.to_csv(OUT_CSV, index=False)


if __name__ == '__main__':
    main()
