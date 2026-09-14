from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import wait
import math

# Initialize Hub and Hardware
hub = PrimeHub()
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.D, Direction.CLOCKWISE)
motor_f = Motor(Port.F)

# DriveBase setup
WHEEL_DIAMETER_MM = 175 / math.pi
AXLE_TRACK_MM = 80  
robot = DriveBase(left_motor, right_motor, wheel_diameter=WHEEL_DIAMETER_MM, axle_track=AXLE_TRACK_MM)

# Enable Gyro for perfectly straight lines and accurate in-place turns
robot.use_gyro(True)

# Define some native Pybricks speeds (mm/s and deg/s) instead of percentages
# (Adjust these based on what your 65%, 50%, etc., translated to)
FAST_SPEED = 300       # roughly 65%
SLOW_SPEED = 50        # roughly 10%
REVERSE_SPEED = 230    # roughly 50%
SLOW_TURN_RATE = 20    # roughly 5% turn speed

# Set global acceleration to be smooth
robot.settings(straight_acceleration=200, turn_acceleration=100)

# ==========================================
# Main Program Loop
# ==========================================

wait(100)
robot.reset()

# Move straight 72 cm (720 mm) at fast speed
robot.settings(straight_speed=FAST_SPEED)
robot.straight(720)

# Turn Left 50 degrees (Negative = Left)
# We set a slow turn_rate beforehand to mimic your custom function
robot.settings(turn_rate=SLOW_TURN_RATE)
robot.turn(-50)

# Move straight 9 cm (90 mm) at slow speed
robot.settings(straight_speed=SLOW_SPEED)
robot.straight(90)

# F run counter-clockwise for 90 degrees
motor_f.run_angle(250, -90, wait=True)

# Move backward 8 cm (-80 mm) at medium speed
robot.settings(straight_speed=REVERSE_SPEED)
robot.straight(-80)

# Turn Right 50 degrees (Positive = Right)
robot.settings(turn_rate=SLOW_TURN_RATE)
robot.turn(50)

# Move backward 72 cm (-720 mm) at fast speed
robot.settings(straight_speed=FAST_SPEED)
robot.straight(-720)

# F run clockwise for 90 degrees
motor_f.run_angle(250, 90, wait=True)
