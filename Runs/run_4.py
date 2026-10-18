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
    drive_base.straight(400)
    set_speed(speed=150)
    drive_base.straight(45)
    drive_base.straight(-45)
    set_speed(speed=800,accel=800)
    drive_base.straight(100) # second
    set_speed(speed=200)
    drive_base.straight(-200)
    drive_base.turn(90)
    left_arm.run_angle(500, -270,wait=False)
    drive_base.straight(450)
    drive_base.use_gyro(False) 
    set_speed(turn_rate=100)
    drive_base.turn(-45)
    wait(500)
    drive_base.straight(30)
    #drive_base.turn(-3)
    set_speed(speed=130)
    drive_base.straight(48) #At the tree
    set_speed(speed=300)
    left_arm.run_angle(600,100,wait=False) #Lift up the seed
    drive_base.straight(-20)
    wait(200)
    #left_arm.run_angle(600,15,wait=False)
    #wait(200)
    drive_base.straight(-100) # Done collecting seed
    # on to next mission 5, reaching roots,
    drive_base.turn(-65)
    drive_base.straight(550) # go to mission 5
    right_arm.run_angle(600,-240) # drop the attache ment
    
    drive_base.use_gyro(True)
    drive_base.turn(30)
    wait(300)
    # TODO: here is where the root mission(5) starts. 
    '''
    right_arm.run_angle(100,-20)
    wait(300)
    drive_base.straight(-30)
    wait(300)
    right_arm.run_angle(100,90)
    '''
    right_arm.run_angle(100,90)
    wait(300)
    drive_base.straight(80)
    wait(300)
    right_arm.run_angle(100,10)
    drive_base.straight(110)
    '''
    drive_base.use_gyro(False)
    drive_base.stop()
    left_arm.stop()
    right_arm.stop()