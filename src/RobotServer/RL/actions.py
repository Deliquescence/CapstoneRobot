import itertools
from bisect import bisect_right


# Exclude 0 so action product doesn't include turns with 0 throttle
positive_throttles = [1]
negative_throttles = list(map(lambda x: x * -1, positive_throttles))
nonnegative_throttles = [0] + positive_throttles

positive_directions = [0, 1]
negative_directions = list(map(lambda x: x * -1, positive_directions))
negative_directions.remove(0)
directions = positive_directions + negative_directions

ACTIONS = [x for x in itertools.product(
    (positive_throttles + negative_throttles), (positive_directions + negative_directions))]
ACTIONS.insert(0, (0, 0))  # Stop

n = len(ACTIONS)


def bucket_throttle(throttle):
    """Return the discretized representation of the given throttle."""
    if throttle < 0:
        return -1 * nonnegative_throttles[bisect_right(nonnegative_throttles, abs(throttle)) - 1]
    else:
        return nonnegative_throttles[bisect_right(nonnegative_throttles, throttle) - 1]


def bucket_direction(direction):
    """Return the discretized representation of the given direction."""
    if direction < 0:
        return -1 * positive_directions[bisect_right(positive_directions, abs(direction)) - 1]
    else:
        return positive_directions[bisect_right(positive_directions, direction) - 1]


def action_from_throttle_direction(throttle, direction):
    """Return the integer action representing the given throttle and direction."""
    throttle = bucket_throttle(throttle)
    if throttle == 0:
        return 0
    else:
        return ACTIONS.index((throttle, bucket_direction(direction)))


def action_to_throttle_direction(action):
    """Return tuple of (throttle, direction) as corresponding to the given integer action index."""

    return ACTIONS[action]


if __name__ == '__main__':
    print(ACTIONS)
    print(n)
