from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from robot import drive_base, left_arm, right_arm, set_speed


hub = PrimeHub()
def run():
    drive_base.use_gyro(True)
    set_speed(speed=250)
    drive_base.straight(358)
    set_speed(turn_rate=200,turn_accel=200, speed=400)
    drive_base.turn(90)    
    drive_base.straight(670)

    #animal drop
    drive_base.turn(45)
    drive_base.straight(100)
    right_arm.run_angle(50,-140)
    drive_base.straight(-110)
    right_arm.run_angle(250,180)
    drive_base.turn(-44.5)
    drive_base.straight(-90)
    drive_base.turn(75)
    drive_base.straight(-120)

    left_arm.run_angle(150,-200)
    drive_base.straight(180)
    left_arm.run_angle(800,370)

    drive_base.turn(-80)
    drive_base.straight(-700)
    left_arm.run_angle(800,90)
    drive_base.stop()
    #left_arm.run_angle(300,-150)


    # begin cane mission

    



