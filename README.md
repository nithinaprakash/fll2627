# fll2627

Pybricks robot code for our FIRST LEGO League 2026-27 season robot (LEGO SPIKE Prime hub).

## Overview

The robot runs a mission picker off of `main.py`. On startup it shows a mission
number on the hub display; the LEFT/RIGHT buttons cycle through missions and
the CENTER button runs the selected one, then returns to the picker - similar
to the standard SPIKE Prime program-slot experience.

## Files

- **`main.py`** - Entry point. Run this on the hub. It imports all mission
  modules and drives the picker loop (button handling, display, mission
  dispatch).
- **`robot.py`** - Shared hardware setup: the hub, drive motors, arm motors,
  and `DriveBase` instance, plus a `set_speed()` helper for adjusting drive
  speed/acceleration/turn settings. Import from here so hardware is only
  initialized once.
- **`mission_1.py` ... `mission_6.py`** - One file per mission, each exposing
  a `run()` function called by the picker in `main.py`.
- **`RockMission.py`** - Standalone mission script, not currently wired into
  the `main.py` picker.
- **`test.py`** - Scratch file with drive-base/motor examples used for
  testing individual movements.
- **`archive/`** - Older/retired mission scripts kept for reference.

## Hardware

Update the ports, directions, wheel diameter, and axle track in `robot.py`
to match your robot's build:

- Left/right drive motors: `Port.E` / `Port.F`
- Left/right arm motors: `Port.A` / `Port.B`
- `WHEEL_DIAMETER_MM` / `AXLE_TRACK_MM`: measured from the robot

## Usage

1. Open this project in the Pybricks IDE and connect to the SPIKE Prime hub.
2. Run `main.py` - it will automatically bundle `robot.py` and all
   `mission_*.py` files.
3. Use LEFT/RIGHT to select a mission number, CENTER to run it.
