# mission_4.py
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

