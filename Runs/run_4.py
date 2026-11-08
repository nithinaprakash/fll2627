from pybricks.hubs import PrimeHub
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
# Our own robot setup (wheels, arms, speed) lives in robot.py
from robot import drive_base, left_arm, right_arm, set_speed
from pybricks.parameters import Stop
def run():  
    hub = PrimeHub()
    drive_base.use_gyro(True)
    #left_arm.run_until_stalled(200, then=Stop.COAST, duty_limit=40)
    #right_arm.run_until_stalled(200, then=Stop.COAST, duty_limit=40)

    set_speed(turn_rate=90, speed=350)  
    drive_base.turn(-85.6)
    drive_base.straight(155)
    drive_base.straight(-50)
    drive_base.straight(75)
    drive_base.straight(-500)

    drive_base.use_gyro(False)
    drive_base.stop()
    left_arm.stop()
    right_arm.stop()
    
