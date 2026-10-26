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
    set_speed(turn_rate=90, speed=350)  
    drive_base.turn(-86)
    set_speed(turn_rate=150)
    #wait(10000)
    drive_base.straight(265) #from 385
    set_speed(speed=150)
    drive_base.straight(45)
    drive_base.straight(-45)
    set_speed(speed=800,accel=800)
    drive_base.straight(90) # second
    set_speed(speed=200)
    drive_base.straight(-172.5)
    drive_base.turn(90)
    left_arm.run_angle(120, -230,wait=False) #270 drop the attachment 
    drive_base.straight(450)
    set_speed(turn_rate=100)
    drive_base.turn(-45) # turn towards the tree
    set_speed(speed=250)
    drive_base.straight(35)
    set_speed(speed=200)
    drive_base.straight(24) # go closer to the tree, some more at lower speed At the tree
    left_arm.run_angle(50,36,wait=False) #Lift up the seed
    drive_base.straight(-10)
    left_arm.run_angle(100,50)
    drive_base.straight(-130) # Done collecting seed
    # on to next mission 5, reaching roots,
    drive_base.turn(-63)
    drive_base.straight(595) # go to mission 5
    right_arm.run_angle(100,-245) # drop the attachment
    #wait(8000)
    drive_base.turn(15)
    right_arm.run_angle(600,260)
    set_speed(speed=600,accel=600)
    drive_base.straight(-800)

    drive_base.use_gyro(False)
    drive_base.stop()
    left_arm.stop()
    right_arm.stop()