
trans_thresh = 6.0
rotate_thresh = 0.35
delay_subtrahend = 3


class TurnController:

    def __init__(self):
        self.in_progress = None

    def get_direction(self, side_translation, tag_rotation, throttle, tz):
        if self.in_progress is None:  # Decide
            if tag_rotation * -1 > rotate_thresh:  # Left?
                if side_translation * -1 > trans_thresh:
                    return 0  # Slightly odd case
                elif side_translation > trans_thresh:
                    self.in_progress = Turn(-1, max(0, tz - delay_subtrahend))
                else:
                    return 0
            elif tag_rotation > rotate_thresh:  # Right?
                if side_translation * -1 > trans_thresh:
                    self.in_progress = Turn(1, max(0, tz - delay_subtrahend))
                elif side_translation > trans_thresh:
                    return 0  # Slightly odd case
                else:
                    return 0
            else:
                if side_translation * -1 > trans_thresh:
                    self.in_progress = Slide(-1)
                elif side_translation > trans_thresh:
                    self.in_progress = Slide(1)
                else:
                    return 0
        
        # Abort operation
        if abs(tag_rotation) < rotate_thresh and abs(side_translation) < trans_thresh:
            self.in_progress = None
            return 0
        # Continue ongoing operation
        direction = self.in_progress.get_direction(throttle)
        if self.in_progress.is_done():
            self.in_progress = None
        return direction


class Slide:

    def __init__(self, direction):
        self.direction = direction
        self.goals = [4, 8, 11]
        self.progress = 0
        self.phase = 0

    def get_direction(self, throttle):
        self.progress += throttle
        direction = self._get_direction()

        if self.progress >= self.goals[self.phase]:
            self.phase += 1

        return direction

    def _get_direction(self):
        if self.phase == 0:  # Begin slide
            return self.direction
        elif self.phase == 2:  # Right ourselves
            return self.direction * -1
        else:
            return 0

    def is_done(self):
        return self.phase >= len(self.goals)


class Turn:
    def __init__(self, direction, dist_delay):
        """
        Init turn command with delay
        :param direction: -1 if left, 1 if right
        :param dist_delay: Distance delay to try and match leader turn initiation location
        """
        self.direction = direction
        self.goal = 11  # Tested under 0.1 sec delay for 90 deg
        self.dist_delay = dist_delay
        self.progress = 0

    def get_direction(self, throttle):
        if self.dist_delay > 0:
            if throttle == 1:
                self.dist_delay -= 1
            elif throttle == -1:
                self.dist_delay += 1
            return 0
        if throttle == 1:
            self.progress += 1
        elif throttle == -1:
            self.progress -= 1

        return self.direction

    def is_done(self):
        return self.progress >= self.goal


def main():
    import picar_driver
    cam = picar_driver.camera
    test_camera(cam)


def test_camera(camera):
    import time
    import follower
    f = follower.Follower()
    while True:
        start = time.monotonic()
        _, frame = camera.read()
        feat = f.get_features(frame)
        x_trans, y_rot = feat[3], feat[1]
        diff = time.monotonic() - start
        print("Translation: %f , Rotation: %f Time %f" % (x_trans, y_rot, diff))


def test_action():
    import time
    import picar_helper
    count = 25  # Fail safe
    tc = TurnController()
    tc.in_progress = Slide(1)
    for _ in range(count):
        direction = tc.get_direction(0, 0, 1, 0)
        picar_helper.move(1, direction)
        if tc.in_progress is None:
            break
        time.sleep(0.1)
    picar_helper.move(0, 0)

if __name__ == '__main__':
    main()


