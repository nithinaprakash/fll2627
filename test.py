from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
ConvertToInch=25
hub = PrimeHub()


# -----------------------------------------------------------------
# SETUP
# -----------------------------------------------------------------
hub = PrimeHub()

# Left and right drive motors.
# Change Port.A / Port.B to match how your robot is actually wired.
# Direction.CLOCKWISE / COUNTERCLOCKWISE depends on which way each
# motor needs to spin for the robot to go "forward" — flip if needed.
left_motor = Motor(Port.E, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.F, Direction.CLOCKWISE)

# Optional third motor for an attachment (e.g. an arm or claw).


# DriveBase needs your wheel diameter and axle track (distance between
# the two wheels' contact points), both in millimeters.
# Measure your own robot and update these two numbers.
WHEEL_DIAMETER_MM = 88
AXLE_TRACK_MM = 110

drive = DriveBase(left_motor, right_motor, WHEEL_DIAMETER_MM, AXLE_TRACK_MM)

# -----------------------------------------------------------------
# BASIC MOTOR CONTROL EXAMPLES (single motors, no DriveBase)
# -----------------------------------------------------------------

def basic_motor_demo():
    # Run a motor at a fixed speed (deg/sec) for a set time.
    left_motor.run(500)          # start spinning at 500 deg/sec
    wait(1000)                   # keep spinning for 1 second
    left_motor.stop()            # coast to a stop

    # Rotate a motor by a specific angle.
    attachment_motor.run_angle(300, 90)  # speed 300 deg/s, turn 90 degrees

    # Rotate to an absolute angle and hold position.
    attachment_motor.run_target(300, 0, then=Stop.HOLD)

    # Run for a fixed duration, and stop by braking (not coasting).
    right_motor.run_time(400, 1500, then=Stop.BRAKE)


# -----------------------------------------------------------------
# DRIVE BASE MOVEMENT EXAMPLES (coordinated two-wheel driving)
# -----------------------------------------------------------------

def drive_square():
    # DriveBase.straight() takes millimeters.
    # DriveBase.turn() takes degrees (positive = clockwise/right).
    #for _ in range(4):

        drive.use_gyro(True)
        #drive.settings()
        #drive.turn(-90)        # turn in place 90 degrees
        #drive.straight(-1000)   # drive forward 200 mm

        #wait(200)
        drive.straight(2*ConvertToInch)   # go straight at 200 mm/s
        drive.turn(90)        # turn in place 90 degrees
        #wait(200)
        drive.use_gyro(False)
        drive.reset


def drive_with_speed_settings():
    # You can set speed/acceleration limits before driving.
    # settings(straight_speed, straight_acceleration, turn_rate, turn_acceleration)
    #drive.settings(straight_speed=300, straight_acceleration=500,
     #               turn_rate=150, turn_acceleration=300)
    #drive.settings()

    #drive.straight(-500)
    drive.turn(-90)  # negative = counterclockwise/left
    #drive.straight(-300)


def manual_drive_loop():
    # Continuous drive/steer control, useful for line following or
    # remote/manual control loops. drive(speed_mm_s, turn_rate_deg_s)
    drive.drive(200, 0)   # go straight at 200 mm/s
    wait(1000)
    drive.drive(150, 45)  # go forward while turning right
    wait(1000)
    drive.stop()          # stop driving


# -----------------------------------------------------------------
# MAIN PROGRAM
# -----------------------------------------------------------------

hub.light.on(Color.GREEN)

drive_square()
#basic_motor_demo()
#drive_with_speed_settings()
hub.light.on(Color.BLUE)
wait(500)