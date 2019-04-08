import time
import numpy as np
import math

from tag_detection.detector import estimate_pose, process_color
from pid import Controller

# Source Version
# https://github.com/Deliquescence/CapstoneRobot/blob/09293d2e6a6550523aa634a71fb05f05a7820c81/src/RobotServer/follower.py

NUM_FEATURES = 22
IDEAL_DISTANCE = 5


class Follower:

    def __init__(self):
        self.controller = Controller(IDEAL_DISTANCE, 0.01)
        self.age_decay = 0.9  # Todo determine good value
        self.reset_state()

    def reset_state(self):
        self.last_state = None
        self.last_tag_state = None
        self.last_action = [0, 0]
        # self.last_self_turn = 99999  # How many frames ago
        # self.last_self_turn_direction = 0  # -1 left, 0 straight, 1 right
        # self.last_turning_state = 0  # -1 left, 0 straight, 1 right

    def get_action(self, frame):
        start_time = time.time()

        pose = estimate_pose(frame)
        if pose is not None:
            rotation, translation, _, _ = pose
            [rx, ry, rz] = rotation
            [tx, ty, tz] = translation
            throttle = self.controller.get_action(tz)
            direction = 0  # Todo allow for turns
        else:  # continue on current path
            throttle, direction = self.last_action

        duration = time.time() - start_time
        # print(f"Prediction took {duration}")

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

    def save(self, file_name=""):
        pass

    @staticmethod
    def load(file_name=""):
        pass
