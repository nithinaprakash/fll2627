# mission_2.py
from robot import drive_base, left_arm, right_arm
from pybricks.tools import wait
from pybricks.parameters import Stop

def run():

    # Example: this mission needs to go faster than the default
    drive_base.settings(straight_speed=600, straight_acceleration=1000,
                         turn_rate=250, turn_acceleration=500)
    drive_base.reset()
    #drive_base.turn(90)
    print("State: Distance, speed, angle, angularspeed", drive_base.state())    
    drive_base.straight(100)
    #wait(1000)
    drive_base.turn(-45)
    drive_base.straight(600)
    drive_base.turn(-45)
    drive_base.straight(80)
    drive_base.straight(-90)
    drive_base.turn(45)
    drive_base.straight(-600)
    drive_base.turn(45)
    drive_base.straight(-100)