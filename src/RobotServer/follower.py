import numpy as np
from PIL import Image
import cv2
import time
import pickle
import math

from RL import states, states, actions, learn
from tag_detection.detector import estimate_pose


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
        self.learner = learn.ActorCritic(np.repeat(0.02, 6), np.repeat(0.8, 5))
        self.last_state = None

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
        return np.zeros(2)  # Todo

    def get_reward(self, frame):
        IDEAL_DISTANCE = 4
        X_THRESHOLD = 10
        Z_THRESHOLD = 30

        weight_tz = 0.9
        weight_tx = 0.075
        weight_ry = 0.025

        pose = estimate_pose(frame)
        if pose is None:
            return 0

        rotation, translation, _, _ = pose
        [_rx, ry, _rz] = rotation
        [tx, _ty, tz] = translation

        # rotation should be 0 (most bad we could actually see is about +/- pi/2)
        ry_error = abs(ry) / (math.pi / 2)
        ry_reward = 1 - ry_error

        # x translation should be 0
        tx = abs(tx)
        if tx > X_THRESHOLD:
            tx_reward = 0
        else:
            tx_reward = 1 - (tx / X_THRESHOLD)

        # follow distance should be reasonable
        if tz > Z_THRESHOLD:
            tz_reward = 0
        else:
            tz_error = abs(IDEAL_DISTANCE - tz) / Z_THRESHOLD
            tz_reward = 1 - tz_error

        return (tz_reward * weight_tz) + (tx_reward * weight_tx) + (ry_reward * weight_ry)



if __name__ == '__main__':
    follower = Follower()
    #image = cv2.imread("~/Pictures/mirrorB_2605.jpg")
    camera = cv2.VideoCapture(0)

    while True:
        _, image = camera.read()
        #action = follower.get_action(image)
        #print(action[0], '\t', action[1])
        reward = follower.get_reward(image)
        print(reward)
