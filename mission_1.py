# mission_1.py
from robot import drive_base, left_arm, right_arm , set_speed
from pybricks.parameters import Stop

def run():
    
    set_speed(350)
    drive_base.reset()
    drive_base.use_gyro(True)
    drive_base.hold()
    print(" drive base start \n",drive_base.distance(),"mm")

    drive_base.straight(100,then=Stop.NONE)
    print(" drive base 1 \n",drive_base.distance(),"mm")
    #drive_base.straight(-25,then=Stop.NONE)
    #drive_base.reset()
    #set_speed(150)
    #drive_base.straight(100)
    set_speed(turn_rate=200,turn_accel=100)
    drive_base.turn(-30)
    set_speed(50)
    drive_base.straight(65)
    drive_base.straight(-25)
    set_speed(turn_accel=400)
    #drive_base.turn(10)
    drive_base.turn(-30)
    left_arm.run_angle(400, -50)
    left_arm.run_angle()
    left_arm.run_angle(100, 50)
    set_speed(turn_rate=50, turn_accel=100)
    drive_base.turn(60)
    set_speed(200)
    drive_base.straight(-700)
    print(" drive base 2\n",drive_base.distance(),"mm")
    print("done\n")