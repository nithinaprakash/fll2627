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
    # start driving toward the drone mission
    drive_base.straight(600)    
    #drive_base.turn()
    drive_base.straight(-100)
    drive_base.turn(-90)
    drive_base.straight(575)
    drive_base.turn(-90) 
    drive_base.straight(50) 
    drive_base.straight(-300) #bumping into skylight to close the roof
    # double bump
    drive_base.straight(50)
    drive_base.straight(-100)
    #drive_base.straight(80)
    #drive_base.straight(-150)
    drive_base.straight(155)
    # turn toward the vine
    drive_base.turn(68)
    right_arm.run_angle(250,-260)
    # go towards the vine
    set_speed(speed=300)
    drive_base.straight(150)
    drive_base.turn(15)  
    right_arm.run_angle(200,75)
    set_speed(speed=800)
    drive_base.straight(-150)
    drive_base.turn(-15)
    right_arm.run_angle(100,-65)
    drive_base.straight(-330)
    right_arm.run_angle(400,70,wait=False)
    drive_base.turn(104)
    set_speed(800)
   # right_arm.run_angle(200,70,wait=False)
    drive_base.arc(1000,distance=900)
  #  drive_base.straight(900)
  #  drive_base.turn(90)
  #  drive_base.straight(250)
    drive_base.stop()
    left_arm.stop()
    right_arm.stop()
    '''
    #come home
   # drive_base.turn(-75)
    #right_arm.run_angle(100,250,wait=False)
    #drive_base.straight(700)
    '''
    '''
    drive_base.turn(-73)
    drive_base.straight(300)
    drive_base.turn(-60)
    right_arm.run_angle(100,250,wait=False)
    drive_base.straight(500)
    '''



    drive_base.use_gyro(False)