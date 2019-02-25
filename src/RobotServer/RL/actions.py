
from enum import Enum

n = 21


class Action(Enum):
    stop = 0

    # throttle_turn
    low_hard_left = 1
    high_hard_left = 2
    low_soft_left = 3
    high_soft_left = 4

    low_straight = 5
    high_straight = 6

    low_soft_right = 7
    high_soft_right = 8
    low_hard_right = 9
    high_hard_right = 10

    rev_low_hard_left = 11
    rev_high_hard_left = 12
    rev_low_soft_left = 13
    rev_high_soft_left = 14

    rev_low_straight = 15
    rev_high_straight = 16

    rev_low_soft_right = 17
    rev_high_soft_right = 18
    rev_low_hard_right = 19
    rev_high_hard_right = 20


STOP_THRESHOLD = 0.01
LOW_THRESHOLD = 0.4

STRAIGHT_THRESHOLD = 0.1
SOFT_THRESHOLD = 0.5


def from_throttle_direction(throttle, direction):
    """Return the action representing the given throttle and direction."""

    if throttle < -1*LOW_THRESHOLD:
        actions = [Action.rev_high_hard_left, Action.rev_high_soft_left,
                   Action.rev_high_straight, Action.rev_high_soft_right, Action.rev_high_hard_right]

    elif throttle < -1*STOP_THRESHOLD:
        actions = [Action.rev_low_hard_left, Action.rev_low_soft_left,
                   Action.rev_low_straight, Action.rev_low_soft_right, Action.rev_low_hard_right]

    elif throttle <= STOP_THRESHOLD:
        actions = [Action.stop]*5

    elif throttle <= LOW_THRESHOLD:
        actions = [Action.low_hard_left, Action.low_soft_left,
                   Action.low_straight, Action.low_soft_right, Action.low_hard_right]

    else:
        actions = [Action.high_hard_left, Action.high_soft_left,
                   Action.high_straight, Action.high_soft_right, Action.high_hard_right]

    if direction < -1*SOFT_THRESHOLD:
        return actions[0]
    elif direction < -1*STRAIGHT_THRESHOLD:
        return actions[1]
    elif direction <= STRAIGHT_THRESHOLD:
        return actions[2]
    elif direction <= SOFT_THRESHOLD:
        return actions[3]
    else:
        return actions[4]


THROTTLE_LOW = 0.5
THROTTLE_HIGH = 1

DIRECTION_SOFT = 0.5
DIRECTION_HARD = 1


def to_throttle_direction(action):
    """Return list of [throttle, direction] as according to the given Action"""

    if action == Action.stop:
        return [0, 0]

    # This could be dumb, and it might just be better to make a normal lookup table
    # Low throttle
    if action in [Action.low_soft_right, Action.low_hard_right, Action.low_soft_left, Action.low_hard_left, Action.low_straight]:
        throttle = THROTTLE_LOW
    # Reverse low throttle
    elif action in [Action.rev_low_soft_right, Action.rev_low_hard_right, Action.rev_low_soft_left, Action.rev_low_hard_left, Action.rev_low_straight]:
        throttle = -1*THROTTLE_LOW
    # High throttle
    elif action in [Action.high_soft_right, Action.high_hard_right, Action.high_soft_left, Action.high_hard_left, Action.high_straight]:
        throttle = THROTTLE_HIGH
    # Reverse high throttle
    elif action in [Action.rev_high_soft_right, Action.rev_high_hard_right, Action.rev_high_soft_left, Action.rev_high_hard_left, Action.rev_high_straight]:
        throttle = -1*THROTTLE_HIGH

    # Hard left
    if action in [Action.low_hard_left, Action.high_hard_left, Action.rev_low_hard_left, Action.rev_high_hard_left]:
        direction = -1*DIRECTION_HARD
    # Soft left
    elif action in [Action.low_soft_left, Action.high_soft_left, Action.rev_low_soft_left, Action.rev_high_soft_left]:
        direction = -1*DIRECTION_SOFT
    # Hard right
    elif action in [Action.low_hard_right, Action.high_hard_right, Action.rev_low_hard_right, Action.rev_high_hard_right]:
        direction = DIRECTION_HARD
    # Soft right
    elif action in [Action.low_soft_right, Action.high_soft_right, Action.rev_low_soft_right, Action.rev_high_soft_right]:
        direction = DIRECTION_SOFT
    else:
        direction = 0

    return [throttle, direction]


if __name__ == '__main__':
    print(Action.high_hard_left)
    print(Action.high_hard_left.value)
    print(Action(0))
