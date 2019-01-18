from picar import front_wheels, back_wheels
import picar
import socket

bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()

def move(throttle, direction):
    fw_default = getDefaultAngle(socket.gethostname())
    FW_ANGLE_MAX = fw_default+30
    FW_ANGLE_MIN = fw_default-30
    rear_wheels_enabled = True
    front_wheels_enabled = True

    motor_speed = int(abs(throttle)*100)
    fw_angle = fw_default+(30*(direction))

    if front_wheels_enabled and (fw_angle >= FW_ANGLE_MIN and fw_angle <= FW_ANGLE_MAX):
        fw.turn(fw_angle)
    if rear_wheels_enabled:
        if (throttle > 0.0):
            move_forward(motor_speed)
        elif (throttle < 0.0):
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

def getDefaultAngle(hostname):
    if hostname == 'picarA':
        return 95
    elif hostname == 'picarB':
        return 90

"""
Wheel angle above 90 is to the right, below 90 is to the left
"""