

trans_thresh = 5.0  # Todo real values
rotate_thresh = 5.0


class TurnController:

    def __init__(self):
        self.in_progress = None

    def get_direction(self, state):
        if self.in_progress is None:  # Decide
            pass
        else:  # Continue ongoing operation
            direction = self.in_progress.get_direction()
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

    def __init__self(self, direction):
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


