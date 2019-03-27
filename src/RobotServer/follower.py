import numpy as np
from PIL import Image
import cv2
import time
import math
from pid import Controller

from RL import states, actions, learn
from RL.states import State
from tag_detection.detector import estimate_pose, process_color

NUM_FEATURES = 22
IDEAL_DISTANCE = 20
DEFAULT_FILE_NAME = 'weights.npz'


def unknown_state_cache(previous_state, state):
    """If the current state is not unknown, pass it through.
    If the current state is unknown but the previous state is known, use that.
    If both are unknown, then unknown."""
    if state.tag_is_unknown():
        return state
    elif previous_state.tag_is_unknown():
        return previous_state
    else:
        return state


class Follower:
    def __init__(self):
        self.learner = learn.Q_Learner(epsilon=0.09)
        # self.learner = learn.ActorCritic(np.repeat(0.02, 6), np.repeat(0.8, 5), NUM_FEATURES)
        self.age_decay = 0.9  # Todo determine good value
        # self.controller = Controller(IDEAL_DISTANCE, 0.01)
        self.reset_state()

    def reset_state(self):
        self.last_state = None
        self.last_tag_state = None
        self.last_action = [0, 0]
        self.last_self_turn = 99999  # How many frames ago
        self.last_self_turn_direction = 0  # -1 left, 0 straight, 1 right
        self.last_turning_state = 0  # -1 left, 0 straight, 1 right

    @staticmethod
    def get_state(features, last_self_turn, last_self_turn_direction, last_turning_state):
        ry = None

        if features[6] == 0:  # Tag not found
            tag_state = 0
        else:
            ry = features[1]
            tx = features[3]
            tz = IDEAL_DISTANCE - features[5]
            tag_state = states.tag_state_from_translation(tx, tz)

        # Self turning
        # recently_turned = last_self_turn < 5
        # if recently_turned:
        #     turn_state = last_self_turn_direction
        # else:
        #     turn_state = 0

        # Assume large y rotation indicates lead car turn
        if ry is not None:
            threshold = 0.25
            if ry < -1 * threshold:
                turn_state = -1
            elif ry > threshold:
                turn_state = 1
            else:
                turn_state = 0
        else:
            turn_state = last_turning_state

        state = State(tag_state, turn_state)

        return state

    def get_action(self, frame, online=True):
        start_time = time.time()

        ###
        # Q LEARNING
        ###
        features = self.get_features(frame)

        state = Follower.get_state(features, self.last_self_turn, self.last_self_turn_direction, self.last_turning_state)
        buffered_state = unknown_state_cache(self.last_state, state)

        action = self.learner.policy(buffered_state)
        (throttle, direction) = actions.action_to_throttle_direction(action)

        reward = self.get_reward(features)

        if abs(direction) > 0.001:
            self.last_self_turn = 0
            if direction < 0:
                self.last_turn_direction = -1
            else:
                self.last_turn_direction = 1
        else:
            self.last_self_turn += 1

        if online and self.last_state is not None:
            self.learner.update(self.last_state, self.last_action, reward, buffered_state)

        self.last_action = [throttle, direction]
        self.last_state = state
        self.last_turning_state = state.turning_state

        ###
        # PID
        ###
        # pose = estimate_pose(frame)
        # if pose is not None:
        #     rotation, translation, _, _ = pose
        #     [rx, ry, rz] = rotation
        #     [tx, ty, tz] = translation
        #     throttle = self.controller.get_action(tz)
        #     direction = 0  # Todo allow for turns
        # else:  # continue on current path
        #     throttle, direction = self.last_action

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
        5: Ideal distance - z axis translation
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

        weight_tz = 0.8
        weight_tx = 0.2

        if feature_vector[9] >= 0.35:  # Raw value 0.6
            color_reward = -5
        else:
            color_reward = 0

        if feature_vector[6] == 0:  # Tag not found
            return color_reward

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

        return (tz_reward * weight_tz) + (tx_reward * weight_tx) + color_reward

    def save(self, file_name=DEFAULT_FILE_NAME):
        self.learner.save(file_name)

    @staticmethod
    def load(file_name=DEFAULT_FILE_NAME, epsilon=0.0):
        f = Follower()
        # f.learner = learn.ActorCritic.load(file_name)
        f.learner = learn.Q_Learner.load()
        f.learner.epsilon = epsilon
        return f


def main():
    import picar_driver
    picar_driver.main(start_mode=2)


if __name__ == '__main__':
    main()
