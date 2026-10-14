from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.tools import wait, StopWatch, multitask, run_task
# Our own robot setup (wheels, arms, speed) lives in robot.py
from pybricks.hubs import PrimeHub
from robot import drive_base, left_arm, right_arm, set_speed
from pybricks.parameters import Stop
from pybricks.tools import wait

hub = PrimeHub()
# drone code
def run():
    drive_base.reset()    
    drive_base.use_gyro( True)
    set_speed(speed=200)
    drive_base.straight(680)

    drive_base.turn(-45)
    '''
    drive_base.straight(55)
    drive_base.curve(400,-45)

    drive_base.turn(85)
    drive_base.straight(-770)

    #drive_base.turn(-45)
    drive_base.stop()


    
    # seed collector code
    set_speed(250)
    drive_base.reset()
    
    drive_base.use_gyro(True)
    drive_base.straight(325)
    drive_base.turn(48)
    drive_base.straight(147)
    

    right_arm.run_angle(200, -70, wait=False)
    drive_base.straight(-450)
    right_arm.run_angle(200, 70)

    drive_base.use_gyro(False)
    '''
     # end of seed collector
