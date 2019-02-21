
from enum import Enum


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


if __name__ == '__main__':
    print(State.near_straight)
    print(State.near_straight.value)
    print(State(0))
