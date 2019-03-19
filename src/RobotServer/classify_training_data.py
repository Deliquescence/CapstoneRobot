import cv2
import numpy as np
import pandas as pd
import os
import glob
import time

from tag_detection.detector import estimate_pose
import follower
from follower import Follower
from RL.states import tag_state_from_translation, TAG_STATES
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
CLASSIFIED_CSV_DIR = "classified"


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


def classify_episode(episode_name):
    start_time = time.time()

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
        # print(image_path)
        if not os.path.isfile(image_path):
            print(f"Image file '{image_path}' is missing!")
            return None
        return f.get_features(cv2.imread(image_path))

    episode_df['features'] = episode_df.apply(row_to_features, axis=1)

    # State
    def row_to_state(row):
        features = row['features']
        if features[6] == 0:  # Tag not found
            return 0
        else:
            tx = features[3]
            tz = follower.IDEAL_DISTANCE - features[5]
            return tag_state_from_translation(tx, tz)

    episode_df['state'] = episode_df.apply(row_to_state, axis=1)

    # Action
    episode_df['action'] = episode_df.apply(lambda row: action_from_throttle_direction(
        row['throttle'], row['direction']), axis=1)

    # Reward
    episode_df['reward'] = episode_df.apply(lambda row: f.get_reward(row['features']), axis=1)

    episode_df[['image_file', 'state', 'action', 'reward']].to_csv(os.path.join(CLASSIFIED_CSV_DIR, episode_name + '.csv'), index=False)
    duration = time.time() - start_time
    print(f"Classification took {duration}s\t for '{episode_name}'")
    print("State counts:", episode_df['state'].value_counts(), sep='\n')

    return episode_df


def classify_all_csvs():
    start_time = time.time()

    dfs = []

    for csv_path in glob.glob(os.path.join(DATA_DIR, '*.csv')):
        episode_name = csv_path.split('\\')[-1].replace('.csv', '')
        dfs.append(classify_episode(episode_name))

    duration = time.time() - start_time
    print(f"Classification took {duration}s\t total for {len(dfs)} episodes")
    return dfs


def load_episode_df(episode):

    if episode.endswith('.csv'):
        csv_path = episode
    else:
        csv_path = os.path.join(CLASSIFIED_CSV_DIR, episode + '.csv')

    if not os.path.isfile(csv_path):
        print(f"No csv for episode '{episode}'")
        return None

    episode_df = pd.read_csv(csv_path)
    # print("State counts:\n", episode_df['state'].value_counts())

    return episode_df


def load_all_classified_df():
    dfs = []

    for csv_path in glob.glob(os.path.join(CLASSIFIED_CSV_DIR, '*.csv')):
        dfs.append(load_episode_df(csv_path))

    return dfs


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


def learn_episodes(learner, dfs):
    for df in dfs:
        learn_episode(learner, df)


def debug_print_Q_state(Q, state):
    print("State", state, TAG_STATES[state])
    print_action_values(Q[state])
    print_best_action(Q[state])


def print_action_values(action_values):
    for a, v in enumerate(action_values):
        print("{0}\t{1}".format(action_to_throttle_direction(a), v))


def print_best_action(action_values):
    print("Best: {0}".format(action_to_throttle_direction(np.argmax(action_values))))


def main():
    os.chdir(BASE_PATH)

    learner = Q_Learner(discount_factor=0.9, alpha=0.5)

    # classify_all_csvs()
    dfs = load_all_classified_df()

    # df = classify_episode('stillB')
    # df = load_episode_df('lineA')

    for _ in range(1):
        learn_episodes(learner, dfs)

    debug_print_Q_state(learner.Q, tag_state_from_translation(0, 30))  # tag_state_from_translation(0, 1)

    n_states = len(TAG_STATES)
    n_unseen_states = 0
    for s in range(n_states):
        if np.array_equal(learner.Q[s], default_action_values()):
            n_unseen_states += 1

    print(f"{n_unseen_states} states have not been seen (out of {n_states})")
    learner.save("q.pkl")


if __name__ == '__main__':
    main()
