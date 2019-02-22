
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


if __name__ == '__main__':
    print(Action.high_hard_left)
    print(Action.high_hard_left.value)
    print(Action(0))
