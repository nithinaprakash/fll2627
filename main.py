# main.py
# Run THIS file. Pybricks will automatically bundle robot.py, mission_1.py,
# mission_2.py, and mission_3.py along with it since they're imported below.
#
# LEFT / RIGHT  -> change selected mission number (wraps around)
# CENTER        -> run the selected mission
# After a mission finishes, it returns to the picker - just like SPIKE Prime.
from robot import hub
from pybricks.parameters import Button, Color
from pybricks.tools import wait

import mission_1
import mission_2
import mission_3
import mission_4
import mission_5
import mission_6
import mission_7
hub.system.set_stop_button(Button.BLUETOOTH)
missions = [mission_1, mission_2, mission_3, mission_4, mission_5, mission_6, mission_7]
selected = 0
prev_pressed = set()


def show_slot():
    hub.display.number(selected + 1)
    hub.light.on(Color.WHITE)  # idle color


show_slot()  # show "1" on startup

while True:
    pressed = hub.buttons.pressed()
    just_pressed = pressed - prev_pressed  # fires once per physical press

    if Button.RIGHT in just_pressed:
        selected = (selected + 1) % len(missions)
        print(" right button\n")
        show_slot()

    elif Button.LEFT in just_pressed:
        print(" left button\n")
        selected = (selected - 1) % len(missions)
        show_slot()

    elif Button.CENTER in just_pressed:
        print(" center button\n")
        hub.light.on(Color.GREEN)       # "running" cue
        missions[selected].run()
        show_slot()                      # back to idle + redraw number

    prev_pressed = pressed
    wait(10)