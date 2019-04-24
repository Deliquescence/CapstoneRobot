from simple_pid import PID


class Controller:
    def __init__(self, goal, sample_time):
        self.pid = PID(1, 0.1, 0.05, setpoint=goal)
        self.pid.output_limits = (-1, 1)
        self.pid.sample_time = sample_time

    def get_action(self, current_value):
        return self.pid(current_value)


if __name__ == '__main__':
    controller = Controller(5, 0.01)
    print(controller.get_action(3))

