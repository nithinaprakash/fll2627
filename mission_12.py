# Mission 12 - Forest Elder
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, multitask, run_task
# Our own robot setup (wheels, arms, speed) lives in robot.py
from robot import drive_base, left_arm, right_arm, set_speed
from pybricks.parameters import Stop
from pybricks.tools import wait


def raise_cane():
    # Mission 12, part 1 (20 points): raise the cane until it touches the tree

    # Drive out to the mission
    drive_base.straight(773)
    drive_base.turn(84.5)         # turn right about 90° to face the mission

    # Use the right arm to flick the cane up
    right_arm.run_angle(200, 140) # move the arm down as close as possible to the mat
    drive_base.straight(60)       # inch forward to get under the cane
    right_arm.run_angle(500, -120)  # quickly move the arm back up to flick the cane up


def hook_support_tie():
    # Mission 12, part 2 (10 points): put the support tie around the post
    # TODO: not built yet
    pass


def run():
    hub = PrimeHub()

    # Set how fast the robot drives
    set_speed(speed=300)

    # Do each part of the Forest Elder mission
    raise_cane()
    hook_support_tie()

    # Head back to base - will need to be updated once the support tie pat is implemented
    drive_base.turn(90)           # turn right 90°
    drive_base.straight(750)      # drive back home

    # Stop the wheels so the robot doesn't keep moving
    drive_base.stop()
