from robot import drive_base, left_arm, right_arm, set_speed
from pybricks.parameters import Stop
from pybricks.tools import wait

def run():
    '''
    drive_base.straight(600)
    drive_base.turn(30)
    drive_base
    '''
    wait(200)
    drive_base.use_gyro(True)
    drive_base.reset()
    drive_base.straight(60)
    set_speed(turn_rate=300)
    right_arm.run_angle(100, -100)
    drive_base.straight(-100)
    right_arm.run_angle(100, 100)
    right_arm.run_angle(100, -110)
    drive_base.turn(55)
    drive_base.straight(-650)
    drive_base.turn(-55)
    drive_base.use_gyro(False)
