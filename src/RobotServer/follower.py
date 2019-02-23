import numpy as np
from PIL import Image
import cv2
import time
import pickle

from RL import tag_detector, states, actions


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
        the probabilities for each action in the form of a numpy array of length nA.

    """
    def policy_fn(observation):
        A = np.ones(nA, dtype=float) * epsilon / nA
        best_action = np.argmax(Q[observation])
        A[best_action] += (1.0 - epsilon)
        return A
    return policy_fn


class Follower:
    def __init__(self):
        with open('models/q.pkl', 'rb') as f:
            Q = pickle.loads(f.read())
            self.policy = make_epsilon_greedy_policy(Q, 0, actions.n)

    def get_action(self, frame):
        start_time = time.time()

        state = tag_detector.state_from_frame(frame)
        action = actions.Action(self.policy(state.value))

        duration = time.time() - start_time
        #print(f"Prediction took {duration}")

        return actions.to_throttle_direction(action)


if __name__ == '__main__':
    follower = Follower()
    #image = cv2.imread("~/Pictures/mirrorB_2605.jpg")
    camera = cv2.VideoCapture(0)

    while True:
        _, image = camera.read()
        action = follower.get_action(image)
        print(action[0], '\t', action[1])
