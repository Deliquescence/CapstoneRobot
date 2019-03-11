import numpy as np
from PIL import Image
import cv2
import time
import pickle
import math

from RL import states, actions, learn
from tag_detection.detector import estimate_pose, process_color

NUM_FEATURES = 22
IDEAL_DISTANCE = 5
DEFAULT_FILE_NAME = 'follower.npz'

# From
# https://github.com/dennybritz/reinforcement-learning/blob/master/TD/Q-Learning%20Solution.ipynb
# Under MIT License by Denny Britz
def make_epsilon_greedy_policy(Q, epsilon, nA):
    """
    Creates an epsilon-greedy policy based on a given Q-function and epsilon.

    Args:
        Q: A dictionary that maps from state -> action-values.
            Each value is a numpy array of length nA (see below)
        epsilon: The probability to select a random action . float between 0 and 1.
        nA: Number of actions in the environment.

    Returns:
        A function that takes the observation as an argument and returns
        an action chosen by epsilon greedy.

    """
    def policy_fn(observation):
        A = np.ones(nA, dtype=float) * epsilon / nA
        best_action = np.argmax(Q[observation])
        A[best_action] += (1.0 - epsilon)

        action = np.random.choice(np.arange(len(A)), p=A)
        return action
    return policy_fn


def default_action_values():
    return np.zeros(actions.n)


def unknown_state_cache(previous_state, state):
    """If the current state is not unknown, pass it through.
    If the current state is unknown but the previous state is known, use that.
    If both are unknown, then unknown."""
    if state != states.State.unknown:
        return state
    elif previous_state != states.State.unknown:
        return previous_state
    else:
        return state


class Follower:
    def __init__(self):
        # Todo serialization
        self.learner = learn.ActorCritic(np.repeat(0.02, 6), np.repeat(0.8, 5), NUM_FEATURES)
        self.last_state = None
        self.last_tag_state = None
        self.age_decay = 0.9  # Todo determine good value

    def reset_state(self):
        self.last_state = None
        self.last_tag_state = None

    def get_action(self, frame):
        start_time = time.time()

        state = self.get_features(frame)
        reward = self.get_reward(frame)

        throttle, direction = self.learner.sample_action(state)

        if self.last_state is not None:
            self.learner.update(self.last_state, state, throttle, direction, reward)

        self.last_state = state

        duration = time.time() - start_time
        #print(f"Prediction took {duration}")

        return throttle, direction

    def get_features(self, frame):
        """
        Return numpy array of features.
        Indexes:
        0: x axis rotation
        1: y axis rotation
        2: z axis rotation
        3: x axis translation
        4: y axis translation
        5: z axis translation
        6: 1 if tag was detected, 0 otherwise
        7: Angle to tag
        8: Straight line distance to tag
        9: Image color homogeneity
        10: Bias
        11-20: Features of last tag state if this state is unknown
        """
        # Don't forget to update NUM_FEATURES

        features = np.zeros(NUM_FEATURES)

        pose = estimate_pose(frame)
        features[9] = max(0, process_color(frame) - 0.25)
        features[10] = 1  # Bias
        if pose is not None:
            rotation, translation, _, _ = pose
            [rx, ry, rz] = rotation
            [tx, ty, tz] = translation
            features[0] = rx
            features[1] = ry
            features[2] = rz
            features[3] = tx
            features[4] = ty
            features[5] = IDEAL_DISTANCE - tz
            features[6] = 1
            features[7] = math.atan(tz / tx)
            features[8] = IDEAL_DISTANCE - math.hypot(tz, tx)
            self.last_tag_state = np.array(features[0:NUM_FEATURES // 2])
            # Leave last_tag features as zeros
        elif self.last_tag_state is not None:
            self.last_tag_state *= math.exp(-1 * self.age_decay)
            features[NUM_FEATURES // 2:] = self.last_tag_state

        return features

    def get_reward(self, feature_vector):
        scale_x = 0.1
        scale_z = 0.1

        weight_tz = 0.9
        weight_tx = 0.1

        if feature_vector[9] >= 0.35:  # Raw value 0.6
            color_reward = -5
        else:
            color_reward = 0

        if feature_vector[6] == 0:  # Tag not found
            return color_reward

        tx = feature_vector[3]
        tz = feature_vector[5]

        # x translation should be 0
        tx_error = abs(tx) * scale_x
        tx_reward = max(0, 1 - tx_error)

        # follow distance should be reasonable
        tz_error = abs(tz) * scale_z
        tz_reward = max(0, 1 - tz_error)

        return (tz_reward * weight_tz) + (tx_reward * weight_tx) + color_reward


    def save(self, file_name=DEFAULT_FILE_NAME):
        self.learner.save(file_name)

    @staticmethod
    def load(file_name=DEFAULT_FILE_NAME):
        f = Follower()
        f.learner = learn.ActorCritic.load(file_name)
        return f


if __name__ == '__main__':
    follower = Follower()
    #image = cv2.imread("~/Pictures/mirrorB_2605.jpg")
    camera = cv2.VideoCapture(0)
    while True:
        _, image = camera.read()
        # col = process_color(image)
        # print("Color value: %f" % col)
        # action = follower.get_action(image)
        # print(action[0], '\t', action[1])
        features = follower.get_features(image)
        reward = follower.get_reward(features)
        print(reward)
