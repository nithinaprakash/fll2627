from pybricks.hubs import PrimeHub
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
# Our own robot setup (wheels, arms, speed) lives in robot.py
from robot import drive_base, left_arm, right_arm, set_speed
from pybricks.parameters import Stop

def run():  
    hub = PrimeHub()
    set_speed(turn_rate=100, speed=600, accel=600)
    drive_base.use_gyro(True)
    drive_base.reset()
    drive_base.straight(600)
    #drive_base.turn()
    drive_base.straight(-100)
    drive_base.turn(-90)
    drive_base.straight(575)
    drive_base.turn(-90)
    drive_base.straight(50)
    drive_base.straight(-300)
    #drive_base.straight(80)
    #drive_base.straight(-150)
    drive_base.straight(130)
    drive_base.turn(73)
    right_arm.run_angle(250,-260)
    drive_base.straight(150)
    right_arm.run_angle(200,75)
    drive_base.straight(-150)
    right_arm.run_angle(100,-65)
    set_speed(speed=800)
    drive_base.straight(-500)
    drive_base.turn(-75)
    right_arm.run_angle(100,250,wait=False)
    drive_base.straight(700)
    '''
    drive_base.turn(-73)
    drive_base.straight(300)
    drive_base.turn(-60)
    right_arm.run_angle(100,250,wait=False)
    drive_base.straight(500)
    '''



    drive_base.use_gyro(False)