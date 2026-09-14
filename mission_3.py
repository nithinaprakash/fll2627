# mission_3.py
from robot import drive_base, left_arm, right_arm
from pybricks.parameters import Stop

def run():
    drive_base.settings(
        straight_speed=300,
        straight_acceleration=500,
        turn_rate=150,
        turn_acceleration=300
    )

    #drive_base.straight(400)
    left_arm.run_angle(50, 90) #speed,angle
    right_arm.run_angle(150, 180)
    #drive_base.straight(-400)
    #drive_base.turn(180)