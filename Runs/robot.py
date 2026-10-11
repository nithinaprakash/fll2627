# robot.py
# Shared hardware setup - import from here in every mission file
# so motors/sensors are only created ONCE.

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase

hub = PrimeHub()

# --- Update these ports to match your robot ---
left_wheel = Motor(Port.E, Direction.COUNTERCLOCKWISE)
right_wheel = Motor(Port.F, Direction.CLOCKWISE)
left_arm = Motor(Port.A)
right_arm = Motor(Port.B)
WHEEL_DIAMETER_MM = 55
AXLE_TRACK_MM = 83
def set_speed(speed=300, accel=500, turn_rate=150, turn_accel=300):
    drive_base.settings(straight_speed=speed, straight_acceleration=accel,
                         turn_rate=turn_rate, turn_acceleration=turn_accel)
drive_base = DriveBase(left_wheel, right_wheel, WHEEL_DIAMETER_MM, AXLE_TRACK_MM)