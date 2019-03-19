import cv2
import numpy as np
import pandas as pd
import os
import glob
import time

from tag_detection.detector import estimate_pose
import follower
from follower import Follower
from RL.states import tag_state_from_pose, tag_state_from_translation
from RL.actions import action_from_throttle_direction, action_to_throttle_direction
from RL.learn import Q_Learner
default_action_values = Q_Learner.default_action_values  # Needed for pickle

BASE_PATH = "../../../train_data"
# Data directory:
# DATA_DIR/episode1.csv
# DATA_DIR/episode2.csv
# DATA_DIR/train/episode1_00000.jpg
# DATA_DIR/train/episode2_00000.jpg
DATA_DIR = "data"
OUT_CSV_DIR = "classified"


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


def state_from_image(image):
    image = np.array(image)
    pose = estimate_pose(image)

    return tag_state_from_pose(pose)


def classify_episode(episode_name):
    start_time = time.time()
    os.chdir(BASE_PATH)

    # Read csv
    csv_path = os.path.join(DATA_DIR, episode_name + '.csv')
    if not os.path.isfile(csv_path):
        print(f"No csv for episode '{episode_name}'")
        return None

    episode_df = pd.read_csv(csv_path)

    # Features
    f = Follower()

    def row_to_features(row):
        image_path = os.path.join(DATA_DIR, *row['image_file'].split('/'))
        return f.get_features(cv2.imread(image_path))

    episode_df['features'] = episode_df.apply(row_to_features, axis=1)

    # State
    def row_to_state(row):
        features = row['features']
        tx = features[3]
        tz = follower.IDEAL_DISTANCE - features[5]

        return tag_state_from_translation(tx, tz)

    episode_df['state'] = episode_df.apply(row_to_state, axis=1)

    # Action
    episode_df['action'] = episode_df.apply(lambda row: action_from_throttle_direction(
        row['throttle'], row['direction']), axis=1)

    # Reward
    episode_df['reward'] = episode_df.apply(lambda row: f.get_reward(row['features']), axis=1)

    episode_df[['image_file', 'state', 'action', 'reward']].to_csv(os.path.join(OUT_CSV_DIR, episode_name + '.csv'), index=False)
    duration = time.time() - start_time
    print(f"Classification took {duration}s\t for '{episode_name}'")

    return episode_df


def load_classified_episode_df(episode_name):
    os.chdir(BASE_PATH)

    # Read csv
    csv_path = os.path.join(OUT_CSV_DIR, episode_name + '.csv')
    if not os.path.isfile(csv_path):
        print(f"No csv for episode '{episode_name}'")
        return None

    return pd.read_csv(csv_path)


def learn_episode(learner, episode_df):
    # Initial state
    previous_state = episode_df.iloc[0]['state']
    previous_action = episode_df.iloc[0]['action']

    for index, row in episode_df.iloc[1:].iterrows():
        state = row['state']
        action = row['action']
        reward = row['reward']

        buffered_state = unknown_state_cache(previous_state, state)

        learner.update(previous_state, previous_action, reward, buffered_state)

        previous_action = action
        previous_state = state


def print_action_values(action_values):
    for a, v in enumerate(action_values):
        print("{0}\t{1}".format(action_to_throttle_direction(a), v))
    print_best_action(action_values)


def print_best_action(action_values):
    print("Best: {0}".format(action_to_throttle_direction(np.argmax(action_values))))


def main():
    learner = Q_Learner()

    # df = classify_episode('lineA')
    df = load_classified_episode_df('lineA')

    learn_episode(learner, df)

    print_action_values(learner.Q[0])


def main_():
    os.chdir(BASE_PATH)

    df = pd.DataFrame(columns=['file_name', 'state', 'tz', 'tx'])

    for file_name in os.listdir(IMAGE_DIR):
        file_name_with_folder = "{0}/{1}".format(IMAGE_DIR, file_name)
        img = Image.open(file_name_with_folder)
        img = np.array(img)

        # TODO save and load the pose for each image so we don't have to recalculate every time
        pose = estimate_pose(img)
        state = tag_state_from_pose(pose)

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
