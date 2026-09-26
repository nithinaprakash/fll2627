# mission_1.py
from robot import drive_base, left_arm, right_arm , set_speed
from pybricks.parameters import Stop

def run():
  
    set_speed(250)
    drive_base.reset()
    drive_base.use_gyro(True)
    drive_base.straight(680)

    drive_base.turn(-40)
    drive_base.straight(55)
    drive_base.curve(100,-45)

    drive_base.turn(85)
    drive_base.straight(-770)

    #drive_base.turn(-45)
    drive_base.stop()