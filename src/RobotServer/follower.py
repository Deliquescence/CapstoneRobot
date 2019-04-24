import numpy as np
from PIL import Image
import cv2
import time
import math


from RL import states, actions, learn
from RL.states import State
from tag_detection.detector import estimate_pose, process_color
import turn

NUM_FEATURES = 11
IDEAL_DISTANCE = 17


def unknown_state_cache(previous_state, state):
    """If the current state is not unknown, pass it through.
    If the current state is unknown but the previous state is known, use that.
    If both are unknown, then unknown."""
    if state is not None and not state.tag_is_unknown():
        return state
    elif previous_state is not None and not previous_state.tag_is_unknown():
        # Cache only the tag
        return State(previous_state.tag_state, state.reversing_state)
    else:
        # e.g. state is unknown but previous state is None
        return state


class Follower:
    def __init__(self):
        self.learner = learn.Q_Learner(epsilon=0.09)
        self.turn_controller = turn.TurnController()
        # self.learner = learn.ActorCritic(np.repeat(0.02, 6), np.repeat(0.8, 5), NUM_FEATURES)
        self.age_decay = 0.9  # Todo determine good value
        self.reset_state()

    def reset_state(self):
        self.last_state = None
        self.last_tag_state = None
        self.last_action = [0, 0]
        self.last_reward = 0

    @staticmethod
    def get_state(features, last_action):
        if features[6] == 0:  # Tag not found
            tag_state = 0
        else:
            tx = features[3]
            tz = features[9]
            tag_state = states.tag_state_from_translation(tx, tz)

        reversing = last_action[0] < 0

        state = State(tag_state, reversing)

        return state

    def get_action(self, frame, online=False):

        ###
        # Q LEARNING
        ###
        features = self.get_features(frame)

        state = Follower.get_state(features, self.last_action)
        buffered_state = unknown_state_cache(self.last_state, state)

        action = self.learner.policy(buffered_state)
        (throttle, direction) = actions.action_to_throttle_direction(action)

        reward = Follower.get_reward(features, buffered_state, (throttle, direction))

        if online and self.last_state is not None:
            self.learner.update(self.last_state, self.last_action, self.last_reward, buffered_state)

        self.last_state = state
        self.last_action = [throttle, direction]
        self.last_reward = reward

        ###
        # ACTOR CRITIC
        ###
        # state = self.get_features(frame)
        # reward = self.get_reward(frame)
        #
        # throttle, direction = self.learner.sample_action(state)
        #
        # if self.last_state is not None:
        #     self.learner.update(self.last_state, state, throttle, direction, reward)
        #
        # self.last_state = state

        if self.turn_controller.in_progress is not None:
           # if features[6] == 0:
            #    throttle = 1
            if isinstance(self.turn_controller.in_progress, turn.Turn):
                throttle = 1
        alt_dir = self.turn_controller.get_direction(features[3], features[1], throttle, features[9])
        return throttle, alt_dir

    @staticmethod
    def get_features(frame):
        """
        Return numpy array of features.
        Indexes:
        0: x axis rotation
        1: y axis rotation
        2: z axis rotation
        3: x axis translation
        4: y axis translation
        5: Ideal distance - z axis translation
        6: 1 if tag was detected, 0 otherwise
        7: Angle to tag
        8: Straight line distance to tag
        9: z axis translation
        10: Bias
        """
        # Don't forget to update NUM_FEATURES

        features = np.zeros(NUM_FEATURES)

        pose = estimate_pose(frame)
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
            features[6] = 1  # Tag detection
            features[7] = math.atan(tz / tx)
            features[8] = IDEAL_DISTANCE - math.hypot(tz, tx)
            features[9] = tz

        return features

    @staticmethod
    def get_reward(feature_vector, state, action):
        scale_x = 0.1

        weight_tz = 0.8
        weight_tx = 0.2

        if feature_vector[6] == 0:  # Tag not found
            return 0

        tx = feature_vector[3]
        tz = abs(feature_vector[5])

        # x translation should be 0
        tx_error = abs(tx) * scale_x
        tx_reward = max(0, 1 - tx_error)

        # follow distance should be reasonable
        if tz <= 5:
            tz_reward = 1
        elif tz <= 15:
            tz_reward = 0.3
        else:
            tz_reward = 0

        if (not state.reversing_state) and action[0] < 0:  # Previously was not reversing, then was
            initial_reverse_reward = 0.5
        else:
            initial_reverse_reward = 0

        return (tz_reward * weight_tz) + (tx_reward * weight_tx) + initial_reverse_reward

    def save(self, file_name=None):
        self.learner.save(file_name)

    @staticmethod
    def load(file_name=None, epsilon=0.0):
        f = Follower()
        # f.learner = learn.ActorCritic.load(file_name)
        f.learner = learn.Q_Learner.load(file_name)
        f.learner.epsilon = epsilon
        return f


def main():
    import picar_driver
    picar_driver.main(start_mode=2)


if __name__ == '__main__':
    main()
