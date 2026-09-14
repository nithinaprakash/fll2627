from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import wait
import math

# Initialize the Hub
hub = PrimeHub()

# --- Hardware Setup ---
# The blocks state: "set movement motors to A+B"
# Assuming standard port assignment: A is left, B is right.
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.D, Direction.CLOCKWISE)

# Initialize attachment motor on Port F
motor_f = Motor(Port.F)

# Calculate wheel diameter from "17.5 cm per rotation" (175 mm)
# Circumference = Pi * Diameter
WHEEL_DIAMETER_MM = 175 / math.pi
AXLE_TRACK_MM = 80  # Standard axle track estimate; adjust to match your robot build

robot = DriveBase(left_motor, right_motor, wheel_diameter=WHEEL_DIAMETER_MM, axle_track=AXLE_TRACK_MM)

# Enable the built-in gyro for maintaining straight headings
robot.use_gyro(True)

# --- Helper Functions ---
def percent_to_mm_s(percent):
    """Converts a 0-100% block speed into Pybricks mm/s."""
    # Assuming max motor speed is ~1000 deg/s (2.77 rotations/sec)
    max_speed_mm_s = (1000 / 360) * 175
    return (percent / 100.0) * max_speed_mm_s

def percent_to_turn_rate(percent):
    """Converts a 0-100% block speed into Pybricks turn rate (deg/s)."""
    return (percent / 100.0) * 360

def turn_in_place(target_degrees, direction):
    """Equivalent to the custom 'turnInPlace' block definition."""
    # "set yaw angle to 0"
    hub.imu.reset_heading(0)
    
    # "set movement speed to 5%"
    turn_rate = percent_to_turn_rate(5)
    
    # "set movement acceleration to slow" (approximate with a low value)
    robot.settings(turn_acceleration=100)
    
    if direction.lower() == 'left':
        # Spin left (In Pybricks, positive turn rate is left)
        #robot.drive(0, -turn_rate)
        robot.turn(-target_degrees)
        # Wait until heading reaches target 
        # (Pybricks heading is positive for left turns)
        #while hub.imu.heading() > -target_degrees:
         #   wait(10)
            
    elif direction.lower() == 'right':
        # Spin right (In Pybricks, negative turn rate is right)
        #robot.drive(0, turn_rate)
        robot.turn(target_degrees)
        # Wait until heading reaches target
        # (Pybricks heading is negative for right turns)
        #while hub.imu.heading() < target_degrees:
         #   wait(10)
            
    # "stop moving" and "set movement motors to coast at stop"
    left_motor.brake()
    right_motor.brake()


# ==========================================
# Main Program Loop
# ==========================================

# "wait .1 seconds"
wait(100)

# Reset the heading/yaw to zero before moving
robot.reset()

# "set movement speed to 65%" & "move straight for 72 cm"
robot.settings(straight_speed=percent_to_mm_s(65))
robot.straight(720) # Pybricks uses millimeters (72 cm = 720 mm)

robot.stop()

# "turnInPlace 45.75 'left'"
turn_in_place(50, 'left')

# "set movement 
# speed to 7%" & "move straight for 8 cm"
robot.settings(straight_speed=percent_to_mm_s(10))
robot.straight(90)

# "F run counter-clockwise for 65 degrees"
# By standard Pybricks conventions, counter-clockwise is negative.
motor_f.run_angle(250, -90, wait=True)

# "set movement speed to 50%" & "move backward for 8 cm"
robot.settings(straight_speed=percent_to_mm_s(50))
robot.straight(-80) # Negative distance moves backward

robot.stop()

# "turnInPlace 45.75 'Right'"
turn_in_place(50, 'right')

# "set movement speed to 65%" & "move backward for 72 cm"
robot.settings(straight_speed=percent_to_mm_s(65))
robot.straight(-720)

# "stop moving"
robot.stop()

# "F run clockwise for 65 degrees"
motor_f.run_angle(250, 90, wait=True)