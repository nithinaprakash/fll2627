from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from robot import drive_base, left_arm, right_arm, set_speed
from pybricks.parameters import Stop
from pybricks.tools import wait
def run():
    hub = PrimeHub()
    wait(200)
    drive_base.reset()
    drive_base.use_gyro(True)
    print(f"Starting heading: {hub.imu.heading()}")
    set_speed(speed=300, turn_rate=100)
    drive_base.curve(29*25.4,80)
    #drive_base.straight(3.68945*25.4)
    print(f"Ending heading: {hub.imu.heading()}")
    #Nithin
    set_speed(speed=100)
    drive_base.straight(75)
    drive_base.straight(-35)
    set_speed(speed = 300, turn_rate=800)
    #drive_base.curve(50,40)
    drive_base.turn(40, wait=False)
    wait(200)
    drive_base.straight(-100)
    #drive_base.turn(180)
    drive_base.curve(-29*25.4,80)
    
    #drive_base.turn(-30)
    #drive_base.turn(40)
    
    #drive_base.curve(30,40)
    drive_base.stop()
    #Nithin

    '''
    set_speed(turn_rate=800,turn_accel=800,speed=800,accel=800)
    drive_base.curve(3,30)
    drive_base.turn(-6)
    drive_base.straight(-30)
    drive_base.turn(5)
    drive_base.straight(-10)
    drive_base.stop()
'''
    """set_speed(speed=400,accel=800)
    drive_base.straight(-45)
    drive_base.stop()
    """


