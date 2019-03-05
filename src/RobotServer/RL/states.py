from enum import Enum
from tag_detection.detector import tag_loc

LEFT_THRESHOLD = -50
RIGHT_THRESHOLD = 50
# These were chosen based on 640 width image
NEAR_THRESHOLD = 125 / 640
FAR_THRESHOLD = 70 / 640

n = 10


class State(Enum):
    unknown = 0

    # distance_angle (of lead car)
    good_straight = 1
    near_straight = 2
    far_straight = 3

    good_left = 4
    near_left = 5
    far_left = 6

    good_right = 7
    near_right = 8
    far_right = 9


def state_from_frame(frame):
    """Returns a State indicating the approximate location of the tag in the given frame."""
    return state_from_loc(tag_loc(frame))


def state_from_loc(loc):
    """Returns a State indicating the approximate location of the tag in the given PreciseLocation."""

    if loc is None:
        return State.unknown
    else:
        # Select direction
        if loc.x_pos <= LEFT_THRESHOLD:
            states = [State.far_left, State.good_left, State.near_left]
        elif loc.x_pos >= RIGHT_THRESHOLD:
            states = [State.far_right, State.good_right, State.near_right]
        else:
            states = [State.far_straight, State.good_straight, State.near_straight]

        # Select distance
        if loc.avg_edge_len >= NEAR_THRESHOLD:
            return states[2]
        elif loc.avg_edge_len <= FAR_THRESHOLD:
            return states[0]
        else:
            return states[1]


if __name__ == '__main__':
    print(State.near_straight)
    print(State.near_straight.value)
    print(State(0))
