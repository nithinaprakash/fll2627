from robot import drive_base, left_arm, right_arm, set_speed
from pybricks.parameters import Stop
from pybricks.tools import wait
def run():
    wait(200)
    drive_base.reset()
    drive_base.use_gyro(True)
    set_speed(speed=300, turn_rate=100)
    drive_base.straight(160)
    drive_base.turn(-55)
    drive_base.straight(300)
    right_arm.run_angle(400, -70)
    right_arm.run_angle(400, 70)
    drive_base.straight(-500)
    drive_base.use_gyro(False)




