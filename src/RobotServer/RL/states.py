import math
import itertools
from bisect import bisect_right

z_thresholds = [0, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30]
angle_thresholds = [0, 10, 20, 30, 40, 50, 60]
angle_thresholds_negative = list(map(lambda x: x * -1, angle_thresholds))
angle_thresholds_negative.remove(0)
angle_states = angle_thresholds + angle_thresholds_negative

STATES = [x for x in itertools.product(z_thresholds, angle_states)]
STATES.insert(0, 0)  # Unknown


def state_from_pose(pose):
    """Get the integer state from the pose.
    If pose is None, state == 0.
    Otherwise, it indexes into the list of states, which is generated based on the thresholds."""
    if pose is None:
        return 0

    rotation, translation, _, _ = pose
    [_rx, _ry, _rz] = rotation
    [tx, _ty, tz] = translation

    return state_from_translation(tx, tz)


def state_from_translation(tx, tz):
    # Translations to the right are negative angles
    # 0 translation is 0 angle
    angle = math.degrees(math.atan2(tz, tx)) - 90
    print(angle)

    # Get the lower bound of the threshold bucket.
    # i.e. get largest threshold \in thresholds such that threshold <= tz
    z_state = z_thresholds[bisect_right(z_thresholds, tz) - 1]
    angle_bucket = angle_thresholds[bisect_right(angle_thresholds, abs(angle)) - 1]

    if angle < 0:
        angle_state = -1 * angle_bucket
    else:
        angle_state = angle_bucket

    return STATES.index((z_state, angle_state))
