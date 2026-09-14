# mission_3.py
from robot import drive_base, left_arm, right_arm, set_speed
from pybricks.parameters import Stop
from pybricks.tools import wait

def run():
    set_speed(170)
    wait(250)
    drive_base.reset()
    drive_base.use_gyro(True)
    drive_base.straight(-385)
    set_speed(100)
    drive_base.straight(-50)
    set_speed(300)
    drive_base.straight(450)
    drive_base.use_gyro(False)