
trans_thresh = 5.0  # Todo real values
rotate_thresh = 5.0


class TurnController:

    def __init__(self):
        self.in_progress = None

    def get_direction(self, side_translation, tag_rotation, throttle):
        if self.in_progress is None:  # Decide
            if tag_rotation * -1 > rotate_thresh:  # Left?
                if side_translation * -1 > trans_thresh:
                    return 0  # Slightly odd case
                elif side_translation > trans_thresh:
                    self.in_progress = Turn(-1)
                else:
                    return 0
            elif tag_rotation > rotate_thresh:  # Right?
                if side_translation * -1 > trans_thresh:
                    self.in_progress = Turn(1)
                elif side_translation > trans_thresh:
                    return 0  # Slightly odd case
                else:
                    return 0
            else:
                if side_translation * -1 > trans_thresh:
                    self.in_progress = Slide(1)
                elif side_translation > trans_thresh:
                    return Slide(-1)
                else:
                    return 0
        # Continue ongoing operation
        direction = self.in_progress.get_direction(throttle)
        if self.in_progress.is_done():
            self.in_progress = None
        return direction


class Slide:

    def __init__(self, direction):
        self.direction = direction
        self.goals = [2, 5, 2]  # Todo real values
        self.progress = 0
        self.phase = 0

    def get_direction(self, throttle):
        if throttle == 1:
            self.progress += 1
        elif throttle == -1:
            self.progress -= 1

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

    def __init__(self, direction):
        self.direction = direction
        self.goal = 5  # Todo real value
        self.progress = 0

    def get_direction(self, throttle):
        if throttle == 1:
            self.progress += 1
        elif throttle == -1:
            self.progress -= 1

        return self.direction

    def is_done(self):
        return self.progress >= self.goal


