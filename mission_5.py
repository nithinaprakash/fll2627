# mission_5.py
from robot import drive_base, left_arm, right_arm, set_speed
from pybricks.parameters import Stop
from pybricks.tools import wait

def run():
    
    
    
    set_speed(200)
    wait(250)
    drive_base.reset()
    drive_base.use_gyro(True)
    drive_base.straight(381)
    set_speed(turn_rate=100,turn_accel=100)
    drive_base.turn(90)

    
    set_speed(turn_rate=150,turn_accel=100)
    drive_base.straight(609)
    set_speed(50)
    drive_base.straight(102)
    wait(200)
    drive_base.turn(-15)
    set_speed(110)
    drive_base.straight(-80)
    drive_base.straight(-20)
    drive_base.turn(290)
    set_speed(200)
    drive_base.straight(300)
    drive_base.turn(-47)
    #drive_base.straight(60)
    #drive_base.turn(-28.4)
    set_speed(130,800)
    wait(100)
    drive_base.reset
    drive_base.straight(-500)
    drive_base.straight(120)
    drive_base.turn(-90)
    set_speed(500)
    drive_base.straight(800)
    drive_base.use_gyro(False)


    '''
    drive_base.turn(170)
    set_speed(100)
    drive_base.straight(180)
    drive_base.use_gyro(False)
   '''