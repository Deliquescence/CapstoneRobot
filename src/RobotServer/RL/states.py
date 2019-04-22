import math
import itertools
from bisect import bisect_right


class State:
    def __init__(self, tag_state, reversing_state):
        self.tag_state = tag_state
        self.reversing_state = reversing_state

    def tag_is_unknown(self):
        return self.tag_state == UNKNOWN

    def as_tuple(self):
        return (self.tag_state, self.reversing_state)

    def __eq__(self, other):
        return self.as_tuple() == other.as_tuple()

    def __hash__(self):
        return self.as_tuple().__hash__()

    def __repr__(self):
        return repr(self.as_tuple())

    def __str__(self):
        if self.reversing_state:
            str_reversing = "reversing"
        else:
            str_reversing = "not reversing"

        if self.tag_is_unknown():
            return "[unknown tag, {0: <13}]".format(str_reversing)

        (z, angle) = self.tag_state

        z_index = z_thresholds.index(z)
        if z_index + 1 < len(z_thresholds):
            next_z = z_thresholds[z_index + 1]
            str_z = "{0} <= z < {1}".format(z, next_z)
        else:
            str_z = "{0} <= z".format(z)
        str_z += ','

        if angle <= angle_thresholds_negative[0]:
            angle_which = "right"
        elif angle < angle_thresholds[1]:
            angle_which = "center"
        else:
            angle_which = "left"

        angle = abs(angle)
        angle_index = angle_thresholds.index(abs(angle))

        if angle_which == "center":
            str_angle = "angle < {0} {1}".format(angle_thresholds[1], angle_which)
        elif angle_index + 1 < len(angle_thresholds):
            next_angle = angle_thresholds[angle_index + 1]
            str_angle = "{0} < angle < {1} {2}".format(angle, next_angle, angle_which)
        else:
            str_angle = "{0} < angle ({1})".format(angle, angle_which)
        str_angle += ','

        return "[{0: <14} {1: <23} {2: <13}]".format(str_z, str_angle, str_reversing)


def init():
    global z_thresholds, angle_thresholds, angle_thresholds_negative
    global TAG_STATES, UNKNOWN, STATES, n

    z_thresholds = [0, 10, 17, 23, 30]
    angle_thresholds = [0, 20]
    angle_thresholds_negative = list(map(lambda x: x * -1, angle_thresholds))
    angle_thresholds_negative.remove(0)
    angle_states = angle_thresholds + angle_thresholds_negative

    TAG_STATES = [x for x in itertools.product(z_thresholds, angle_states)]
    UNKNOWN = 0
    TAG_STATES.insert(0, UNKNOWN)  # Unknown

    REVERSING_STATES = [True, False]

    """((z, angle), reversing_state)"""
    STATES = [State(x[0], x[1]) for x in itertools.product(TAG_STATES, REVERSING_STATES)]

    n = len(STATES)

def tag_is_unknown(state):
    """Check if in the given state, the tag is unknown."""
    return state == None or state[0] == UNKNOWN


def tag_state_from_pose(pose):
    """Get representation of tag state from pose."""
    if pose is None:
        return 0

    rotation, translation, _, _ = pose
    [_rx, _ry, _rz] = rotation
    [tx, _ty, tz] = translation

    return tag_state_from_translation(tx, tz)


def tag_state_from_translation(tx, tz):
    """Get representation of tag state from given tx, tz."""
    # Translations to the right are negative angles
    # 0 translation is 0 angle
    angle = math.degrees(math.atan2(tz, tx)) - 90

    # Get the lower bound of the threshold bucket.
    # i.e. get largest threshold \in thresholds such that threshold <= tz
    z_state = z_thresholds[bisect_right(z_thresholds, tz) - 1]
    angle_bucket = angle_thresholds[bisect_right(angle_thresholds, abs(angle)) - 1]

    if angle < 0:
        angle_state = -1 * angle_bucket
    else:
        angle_state = angle_bucket

    return (z_state, angle_state)


init()
if __name__ == '__main__':
    print(STATES)
    print(n)
    for state in STATES:
        print(repr(state), str(state), sep="\t\t")
    print()
