# robot.py
# Shared hardware setup - import from here in every mission file
# so motors/sensors are only created ONCE.

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase 
from pybricks.tools import wait, StopWatch

hub = PrimeHub()

# --- Update these ports to match your robot ---
left_wheel = Motor(Port.E, Direction.COUNTERCLOCKWISE)
right_wheel = Motor(Port.F, Direction.CLOCKWISE)
left_arm = Motor(Port.A,Direction.CLOCKWISE)
right_arm = Motor(Port.B,Direction.COUNTERCLOCKWISE)
WHEEL_DIAMETER_MM = 55
AXLE_TRACK_MM = 83
def set_speed(speed=300, accel=500, turn_rate=150, turn_accel=300):
    drive_base.settings(straight_speed=speed, straight_acceleration=accel,
                         turn_rate=turn_rate, turn_acceleration=turn_accel)
drive_base = DriveBase(left_wheel, right_wheel, WHEEL_DIAMETER_MM, AXLE_TRACK_MM)

pause = wait  # keeps the delay function usable inside lift_arm

from pybricks.tools import wait, StopWatch

def lift(arm, speed=500, angle=90, blocking=False, timeout=800, hold=True):
    a0 = arm.angle()
    arm.run_angle(speed, angle, wait=False)
    if blocking:
        timer = StopWatch()
        while not arm.done() and timer.time() < timeout:
            wait(10)
        elapsed = timer.time()
        print("lift: target", angle, "got", arm.angle() - a0,
              "time", elapsed, "ms",
              "done", arm.done(), "stalled", arm.stalled(),
              "timed_out", elapsed >= timeout)
        if hold:
            arm.hold()
        else:
            arm.stop()
