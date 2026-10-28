from pybricks.hubs import PrimeHub
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
# Our own robot setup (wheels, arms, speed) lives in robot.py
from robot import drive_base, left_arm, right_arm, set_speed, lift
from pybricks.parameters import Stop

def run():  
    hub = PrimeHub()
    drive_base.use_gyro(True)
    drive_base.reset()
    left_arm.run_until_stalled(-200, then=Stop.COAST, duty_limit=40)
    right_arm.run_until_stalled(200, then=Stop.COAST, duty_limit=40)
    left_arm.reset_angle(0)
    right_arm.reset_angle(0)
    ## test
    set_speed(turn_rate=90, speed=250)
    drive_base.turn(45)
    drive_base.straight(370)

    start = left_arm.angle()
    d0 = drive_base.distance()
    print("1 start")
    left_arm.run_angle(500, 186, then=Stop.COAST,wait=False)
    drive_base.straight(-5)
    print("2 backed", drive_base.distance() - d0, "mm, arm at", left_arm.angle() - start)

    left_arm.run_angle(300, 17, then=Stop.COAST)          # absolute: makes up any shortfall
    print("3 arm at", left_arm.angle() - start)

    d1 = drive_base.distance()
    drive_base.straight(-25)
    print("4 backed", drive_base.distance() - d1, "mm")
    #wait(5000)
    '''
    left_arm.run_angle(300, 36, wait=False) #Lift up the seed
    #lift(left_arm,300, 90, wait=False, timeout=150)
    wait(150)
    drive_base.straight(-10,wait=False)
    '''
    left_arm.run_angle(100,49)
    drive_base.straight(-100)
    # turning left toward root
    drive_base.turn(-61) # 62.5
    print("turning less")
    right_arm.run_angle(100,-257,wait=False)
    # go to root
    drive_base.straight(605)
    right_arm.stop()
    wait(500)
    drive_base.turn(22)
    # flick the root
    right_arm.run_angle(730,100)#flicking the root old speed 700
    # not sure if left arm needs to go down. TBD
    left_arm.run_angle(100,-100,wait=False)
    set_speed(speed=300)
    drive_base.straight(-740)

    drive_base.use_gyro(False)
    drive_base.stop()
    left_arm.stop()
    right_arm.stop()