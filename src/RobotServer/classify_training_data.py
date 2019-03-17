import cv2
import numpy as np
import pandas as pd
import os
from PIL import Image

from tag_detection.detector import estimate_pose
from follower import Follower
from RL.states import state_from_pose
from RL.actions import action_from_throttle_direction

BASE_PATH = "../../../train_data"
IMAGE_DIR = "train"
IN_CSV = "labels.csv"  # For the action done
OUT_CSV = "rl_Labels.csv"


def offset_state(df, row, offset):
    try:
        offset_row = df.iloc[row.name + offset]
    except IndexError:
        return 0

    current_name_splits = row['file_name'].split('_')
    offset_name_splits = offset_row['file_name'].split('_')
    if offset_name_splits[0] != current_name_splits[0]:
        # Not same training label
        # print("{} and {} are not same label".format(
        #     offset_name_splits[0], current_name_splits[0]))
        return 0

    current_num = current_name_splits[1].split(".")[0]
    offset_num = offset_name_splits[1].split(".")[0]
    if int(offset_num) != int(current_num) + offset:
        # Not consecutive
        # print("{} and {} are not consecutive".format(offset_num, current_num))
        return 0

    return offset_row['state']


def unknown_state_cache(previous_state, state):
    """If the current state is not unknown, pass it through.
    If the current state is unknown but the previous state is known, use that.
    If both are unknown, then unknown."""
    if state != 0:
        return state
    elif previous_state != 0:
        return previous_state
    else:
        return state


def main():
    os.chdir(BASE_PATH)

    df = pd.DataFrame(columns=['file_name', 'state', 'tz', 'tx'])

    for file_name in os.listdir(IMAGE_DIR):
        file_name_with_folder = "{0}/{1}".format(IMAGE_DIR, file_name)
        img = Image.open(file_name_with_folder)
        img = np.array(img)

        # TODO save and load the pose for each image so we don't have to recalculate every time
        pose = estimate_pose(img)
        state = state_from_pose(pose)

        if pose is None:
            tz = None
            tx = None
        else:
            _rotation, translation, _, _ = pose
            [tx, _ty, tz] = translation

        logging = False
        if logging:
            print(file_name)
            print(tz, tx)
            print(state)

        df = df.append(
            {'file_name': file_name_with_folder, 'state': state, 'tz': tz, 'tx': tx}, ignore_index=True)

    print(df['state'].value_counts())
    print(df)

    df = df.merge(
        pd.read_csv(IN_CSV), left_on="file_name", right_on="image_file", how="inner", validate="1:1")

    df['action'] = df.apply(lambda row: action_from_throttle_direction(
        row['throttle'], row['direction']), axis=1)

    try:
        follower = Follower.load()
    except IOError:  # file does not exist
        follower = Follower()

    # TODO handle episodes
    # TODO save and load the pose for each image so we don't have to recalculate every time
    def row_to_reward(row):
        frame = cv2.imread(row['file_name'])
        features = follower.get_features(frame)
        return follower.get_reward(features)

    df['reward'] = df.apply(row_to_reward, axis=1)

    # One state unknown buffer
    df['state'] = df.apply(lambda row: unknown_state_cache(
        offset_state(df, row, -1), row['state']), axis=1)

    # Save tag classifications for manual inspection
    df[['file_name', 'state', 'throttle', 'direction', 'action']].to_csv(
        "categorized.csv", index=False)

    # Unknown latch
    # for index, row in df.iterrows():
    #     row['state'] = unknown_state_cache(offset_state(df, row, -1), row.state)
    #     df.loc[index, 'state'] = row.state

    df['next_state'] = df.apply(lambda row: offset_state(df, row, 1), axis=1)

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

    # print(rl_labels)
    print(rl_labels['state'].value_counts())
    rl_labels.to_csv(OUT_CSV, index=False)


if __name__ == '__main__':
    main()
