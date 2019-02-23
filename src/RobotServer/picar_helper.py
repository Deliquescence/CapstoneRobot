from picar import front_wheels, back_wheels
import socket

bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
hostname = socket.gethostname()


def move(throttle, direction):
    fw_default = getDefaultAngle()
    fw_angle_max = fw_default + 30
    fw_angle_min = fw_default - 30
    rear_wheels_enabled = True
    front_wheels_enabled = True

    motor_speed = int(abs(throttle) * 100)
    fw_angle = fw_default + (30 * direction)

    if front_wheels_enabled and (fw_angle_min <= fw_angle <= fw_angle_max):
        fw.turn(fw_angle)
    if rear_wheels_enabled:
        if throttle > 0.0:
            move_forward(motor_speed)
        elif throttle < 0.0:
            move_backward(motor_speed)
        else:
            stop()


def move_forward(speed):
    bw.speed = speed
    bw.backward()


def move_backward(speed):
    bw.speed = speed
    bw.forward()


def stop():
    bw.stop()


def getDefaultAngle():
    return 90


"""
Wheel angle above 90 is to the right, below 90 is to the left
"""
