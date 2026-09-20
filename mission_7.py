from robot import drive_base, left_arm, right_arm, set_speed
from pybricks.parameters import Stop
from pybricks.tools import wait

def run():
    wait(200)
    drive_base.use_gyro(True)
    drive_base.reset()
    set_speed(speed=300, accel=600, turn_rate=100, turn_accel=250)
    drive_base.straight(40)
    drive_base.turn(-53)
    drive_base.straight(495)
    drive_base.turn(53)
    set_speed(speed=175, accel=250)
    drive_base.straight(140)
    drive_base.turn(-90)
    drive_base.straight(86)
    drive_base.use_gyro(False)

    '''
    drive_base.turn(-37)
    set_speed(turn_accel=300, speed=100)
    drive_base.straight(30)
    drive_base.use_gyro(False)
    '''
