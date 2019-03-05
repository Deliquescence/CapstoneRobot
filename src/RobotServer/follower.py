import numpy as np
from PIL import Image
import cv2
import time
import pickle

from RL import states, states, actions, learn


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
        return 0  # Todo


if __name__ == '__main__':
    follower = Follower()
    #image = cv2.imread("~/Pictures/mirrorB_2605.jpg")
    camera = cv2.VideoCapture(0)

    while True:
        _, image = camera.read()
        action = follower.get_action(image)
        print(action[0], '\t', action[1])
