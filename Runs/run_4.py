from pybricks.hubs import PrimeHub
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.tools import wait, StopWatch, multitask, run_task
# Our own robot setup (wheels, arms, speed) lives in robot.py
from robot import drive_base, left_arm, right_arm, set_speed
from pybricks.parameters import Stop
from pybricks.tools import wait
def run():  
    hub = PrimeHub()
    drive_base.reset()    
    drive_base.use_gyro(True)
    set_speed(speed=350)
    drive_base.straight(385)
    set_speed(speed=150)
    drive_base.straight(45)
    drive_base.straight(-45)
    set_speed(speed=800,accel=800)
    drive_base.straight(100) # second
    set_speed(speed=200)
    drive_base.straight(-200)
    drive_base.turn(90)
    left_arm.run_angle(120, -230,wait=False) #270 drop the attachment 
    drive_base.straight(450)
    set_speed(turn_rate=100)
    drive_base.turn(-45) # turn towards the tree
    set_speed(speed=250)
    drive_base.straight(46) # go closer to the tree, some more at lower speed At the tree
    left_arm.run_angle(100,50) #Lift up the seed
    drive_base.straight(-20)
    left_arm.run_angle(100,50)
    drive_base.straight(-120) # Done collecting seed
    # on to next mission 5, reaching roots,
    drive_base.turn(-61)
    drive_base.straight(590) # go to mission 5
    right_arm.run_angle(120,-260) # drop the attachment
    drive_base.turn(23)
    right_arm.run_angle(400,260)
    set_speed(speed=600,accel=600)
    drive_base.straight(-800)
    '''drive_base.straight(-50)
    drive_base.straight(55)
    right_arm.run_angle(300,-30)
    drive_base.straight(-50)
    right_arm.run_angle(100,140,wait=False)
    wait(500)
    set_speed(speed=100)
    drive_base.straight(200)
    drive_base.straight(-100)

    set_speed(speed=500, accel = 500)
    drive_base.straight(-800)
    '''

    '''
    wait(300)
    right_arm.run_angle(100,-20)
    wait(300)
    drive_base.straight(-30)
    wait(300)
    right_arm.run_angle(100,90)
    
    right_arm.run_angle(100,90)
    wait(300)
    drive_base.straight(80)
    wait(300)
    right_arm.run_angle(100,10)
    drive_base.straight(110)
    drive_base.use_gyro(False)
    '''
    drive_base.stop()
    left_arm.stop()
    right_arm.stop()