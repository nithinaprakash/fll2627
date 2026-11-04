"""
coqui_demo.py - a simple, talkative Coqui Finder that shows which way a sound came from.

It listens with the four microphones on the reSpeaker board, works out the direction
of each loud sound, and prints the answer step by step so you can see how it works.

To run it (in a terminal, in the folder with this file):

    pip install numpy sounddevice pyusb libusb-package
    python coqui_demo.py

Press Ctrl+C to stop.
"""
import sys

import numpy as np

# =============================================================================
# 1. SETTINGS - the only part you should need to change
# =============================================================================
BOARD = "xvf3800"         # "xvf3000" (the older board) or "xvf3800" (the newer one)

SPEED_OF_SOUND = 343.0    # metres per second, at about 20 °C
SAMPLE_RATE = 16000       # the board records 16,000 samples every second
CHUNK_SECONDS = 0.5       # how much sound we look at each time
LOWEST_PITCH = 900        # coqui calls are between these two pitches (Hz),
HIGHEST_PITCH = 2500      # so we ignore everything else (traffic, voices...)
LOUDER_THAN_QUIET_BY = 6  # a sound must be this many dB louder than the quiet room
MIN_SOUND_DB = 55         # ...and at least this loud at the board
MIN_AGREEMENT = 0.5       # how much the 6 mic pairs must agree (0 to 1)
HOLD_SECONDS = 5          # keep each answer on screen this long before showing a new one

# Lining up with the chalk circle (the clap test). Each board has its own numbers,
# because each one sits in a different mount. Change only your board's numbers:
#   1. Clap on the 0° chalk line. Put the "board angle" it prints into ZERO_DEGREES.
#   2. Clap on the 90° chalk line. If it doesn't say about 90°, flip CLOCKWISE.
ZERO_DEGREES_FOR = {"xvf3000": 136, "xvf3800": -136}
CLOCKWISE_FOR = {"xvf3000": True, "xvf3800": True}

ZERO_DEGREES = ZERO_DEGREES_FOR[BOARD]   # the numbers for the board chosen above
CLOCKWISE = CLOCKWISE_FOR[BOARD]

# Matching our dB numbers to a sound meter:
#   Play a steady sound, hold the meter next to the board, and compare.
#   If our number is 4 dB too low, add 4 to FULL_SCALE_DB (too high: subtract).
FULL_SCALE_DB = 120

# The ring of 12 lights on the board (one light every 30°). Each board has its own
# settings, because the lights sit differently on each one.
# Clap from different sides and watch which light turns red:
#   - If the red light is a few lights away from you, change LED_SHIFT by that many
#     (try +1 first; if it gets worse, go the other way).
#   - If the light moves the opposite way to you as you walk around, flip LED_REVERSE.
USE_LEDS = True
LED_SHIFT = {"xvf3000": -5, "xvf3800": 6}
LED_REVERSE = {"xvf3000": True, "xvf3800": False}

# Where each microphone sits, in metres from the centre of the board,
# and which recording channel it is on. Mic letters A-D are just names.
BOARDS = {
    "xvf3000": {   # 4 mics on a circle, 64 mm across
        "positions": [(-0.032, 0.0), (0.0, -0.032), (0.032, 0.0), (0.0, 0.032)],
        "channels": [1, 2, 3, 4],     # channels 2-5 in the manual (Python counts from 0)
    },
    "xvf3800": {   # 4 mics on the corners of a 66 mm square
        "positions": [(0.033, -0.033), (0.033, 0.033), (-0.033, 0.033), (-0.033, -0.033)],
        "channels": [2, 3, 4, 5],     # channels 3-6 in the manual
    },
}
MIC_NAMES = ["A", "B", "C", "D"]


# =============================================================================
# 2. THE ANSWER KEY - made once, before we start listening
# =============================================================================
# For every direction (0°, 1°, 2° ... 359°) we work out how much earlier or later
# the sound should reach each mic. Distance = speed x time, so time = distance / speed.
mics = np.array(BOARDS[BOARD]["positions"])
pairs = [(i, j) for i in range(4) for j in range(i + 1, 4)]   # 6 pairs: AB AC AD BC BD CD


def arrival_times(direction_deg):
    """When the sound reaches each mic (in seconds) if it comes from this direction.
    The mic nearest the sound gets it first, so it has the smallest number."""
    a = np.radians(direction_deg)
    toward_sound = np.array([np.cos(a), np.sin(a)])
    head_start = mics @ toward_sound        # metres closer to the sound than the centre is
    return -head_start / SPEED_OF_SOUND


def build_answer_key():
    key = np.zeros((360, len(pairs)))       # one row per direction, one column per pair
    for d in range(360):
        t = arrival_times(d)
        key[d] = [t[i] - t[j] for i, j in pairs]
    return key


# =============================================================================
# 3. GRADING A CHUNK OF SOUND AGAINST THE ANSWER KEY
# =============================================================================
ZOOM = 16   # measure timing 16x finer than the gap between two samples


def pair_timing_curves(sound):
    """For each mic pair, a curve saying how well the two recordings line up
    at each possible time gap. We keep only the timing (not the loudness),
    and only the coqui pitches."""
    n = 2 * len(sound)
    spectra = np.fft.rfft(sound, n=n, axis=0)
    pitches = np.fft.rfftfreq(n, 1 / SAMPLE_RATE)
    keep = (pitches >= LOWEST_PITCH) & (pitches <= HIGHEST_PITCH)
    curves = []
    for i, j in pairs:
        cross = spectra[:, i] * np.conj(spectra[:, j])
        cross = cross / (np.abs(cross) + 1e-12)        # throw away loudness, keep timing
        cross[~keep] = 0
        curves.append(np.fft.irfft(cross, n=n * ZOOM))
    return curves, n * ZOOM


def best_direction(sound, key):
    """Grade the sound against all 360 rows of the answer key and pick the best."""
    curves, length = pair_timing_curves(sound)
    fine_rate = SAMPLE_RATE * ZOOM
    scores = np.zeros(360)
    best_possible = 0.0
    for p, curve in enumerate(curves):
        gaps = np.round(key[:, p] * fine_rate).astype(int) % length
        scores += curve[gaps]                 # how well this pair agrees with each direction
        best_possible += curve.max()
    best = int(np.argmax(scores))
    agreement = max(0.0, scores[best] / best_possible) if best_possible > 0 else 0.0
    return best, agreement


def loudness_db(sound):
    """How loud the sound is at the board, in dB (the scale a sound meter uses)."""
    sound = sound - sound.mean(axis=0)
    rms = np.sqrt(np.mean(sound ** 2)) + 1e-12
    return 20 * np.log10(rms) + FULL_SCALE_DB


def to_chalk(board_angle):
    """Turn the board's own angle into the angle on the chalk circle."""
    turned = board_angle - ZERO_DEGREES
    return round(-turned if CLOCKWISE else turned) % 360


# =============================================================================
# 4. PRINTING THE ANSWER
# =============================================================================
def draw_compass(chalk_angle):
    """A little picture: the board (O) in the middle, F where the sound came from.
    0° is at the top and 90° on the right, like the chalk circle seen from above."""
    rows, cols, r = 11, 31, 5
    grid = [[" "] * cols for _ in range(rows)]
    cy, cx = rows // 2, cols // 2
    a = np.radians(chalk_angle)
    for step in np.linspace(0.25, 1.0, 8):
        y = int(round(cy - step * r * np.cos(a)))
        x = int(round(cx + step * 2 * r * np.sin(a)))
        grid[y][x] = "F" if step == 1.0 else "·"
    grid[cy][cx] = "O"
    lines = [" " * 5 + " " * cx + "0"]
    for k, row in enumerate(grid):
        text = "".join(row)
        lines.append(("270  " + text + "  90") if k == cy else (" " * 5 + text))
    lines.append(" " * 5 + " " * (cx - 1) + "180")
    return "\n".join(lines)


def explain(board_angle, agreement, level, floor):
    chalk_angle = to_chalk(board_angle)
    t = arrival_times(board_angle)
    order = np.argsort(t)
    print("\n")
    print(f"  Heard something!  {level:.0f} dB at the board "
          f"({level - floor:.0f} dB louder than the quiet room)")
    print("  Graded it against all 360 directions in the answer key.")
    print(f"  Best match: {chalk_angle}°   (board angle {board_angle}°, "
          f"the 6 mic pairs agree {agreement:.0%})")
    print("  That direction means the sound reached the mics in this order:")
    for rank, m in enumerate(order):
        print(f"     {rank + 1}. mic {MIC_NAMES[m]}   +{(t[m] - t[order[0]]) * 1000:.2f} ms")
    print(draw_compass(chalk_angle))


# =============================================================================
# 5. THE LIGHTS
# =============================================================================
class Lights:
    """Talks to the 12 lights over USB. If anything is missing, it just turns itself off.
    The two boards understand different light commands, so each has its own way to send."""

    USB_IDS = {"xvf3000": 0x0018, "xvf3800": 0x001A}   # product numbers (the maker is 0x2886)

    def __init__(self):
        self.dev = None
        if not USE_LEDS:
            return
        try:
            try:
                import libusb_package          # brings its own copy of libusb (like Seeed's tool)
                self.dev = libusb_package.find(idVendor=0x2886, idProduct=self.USB_IDS[BOARD])
            except ImportError:
                import usb.core                # otherwise use the Mac's libusb (brew install libusb)
                self.dev = usb.core.find(idVendor=0x2886, idProduct=self.USB_IDS[BOARD])
        except Exception as e:
            print(f"Lights: off (could not load pyusb/libusb: {e})")
            return
        if self.dev is None:
            print(f"Lights: off (could not find the {BOARD}'s light controller)")
            return
        print(f"Lights: ready ({BOARD})")

    def send(self, command, group, data):
        """Send one light command. 0x40 means "a special command for this device"."""
        if self.dev is None:
            return
        try:
            self.dev.ctrl_transfer(0x40, 0, command, group, data, 8000)
        except Exception as e:
            print(f"\nLights: stopped working ({e})")
            self.dev = None

    def show(self, colours):
        """Set all 12 lights. colours is a list of 12 (red, green, blue) values, 0-255."""
        if BOARD == "xvf3000":
            data = []
            for r, g, b in colours:
                data += [r, g, b, 0]           # each light gets 4 numbers: red, green, blue, unused
            self.send(6, 0x1C, data)           # command 6 = "show these colours"
        else:
            self.send(12, 20, [5])             # light mode 5 = "ring": each light its own colour
            data = []
            for r, g, b in colours:            # each light is one number 0xRRGGBB, sent as 4 bytes
                data += list(((r << 16) | (g << 8) | b).to_bytes(4, "little"))
            self.send(19, 20, data)            # command 19 = "ring colours"

    def point(self, board_angle, bright=True):
        """Light the one light facing the sound, with dim neighbours either side."""
        steps = round(board_angle / 30)
        if LED_REVERSE[BOARD]:
            steps = -steps
        facing = (steps + LED_SHIFT[BOARD]) % 12
        main, side = ((160, 0, 0), (20, 0, 0)) if bright else ((25, 0, 0), (0, 0, 0))
        colours = [(0, 0, 0)] * 12
        colours[facing] = main
        colours[(facing - 1) % 12] = side
        colours[(facing + 1) % 12] = side
        self.show(colours)

    def off(self):
        """Turn all the lights off (they come back to normal when the board is replugged)."""
        if BOARD == "xvf3000":
            self.send(1, 0x1C, [0, 0, 0, 0])   # command 1 = "make every light this one colour"
        else:
            self.send(12, 20, [0])             # light mode 0 = off


# =============================================================================
# 6. LISTENING
# =============================================================================
def chunks_from_board():
    try:
        import sounddevice as sd
    except ImportError:
        sys.exit("Please install sounddevice first:   pip install sounddevice")
    device = None
    for i, d in enumerate(sd.query_devices()):
        if any(w in d["name"].lower() for w in ("respeaker", "xvf", "4-mic")) and d["max_input_channels"] >= 6:
            device = i
            print(f"Found the board: {d['name']}")
            break
    if device is None:
        sys.exit("Can't find the reSpeaker board with 6 channels. Is it plugged in?\n"
                 "On a Mac, also check System Settings > Privacy & Security > Microphone.")
    size = int(CHUNK_SECONDS * SAMPLE_RATE)
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=6, dtype="int16",
                        device=device, blocksize=size) as stream:
        while True:
            data, _ = stream.read(size)
            yield data.astype(float) / 32768


def listen(chunks, key, lights, quiet_rounds=4):
    channels = BOARDS[BOARD]["channels"]
    floor = None
    show_next_after = 0.0      # time (in seconds of sound) when we may show a new answer
    last_angle = None
    print(f"\nFirst, measuring how loud the quiet room is (stay quiet for {quiet_rounds * CHUNK_SECONDS:.0f} s)...")
    for n, chunk in enumerate(chunks):
        now = n * CHUNK_SECONDS
        holding = now < show_next_after
        if not holding and last_angle is not None:
            lights.point(last_angle, bright=False)   # dim the light: ready for a new answer
            last_angle = None
        sound = chunk[:, channels]
        level = loudness_db(sound)

        if n < quiet_rounds:                   # learning what "quiet" sounds like
            floor = level if floor is None else min(floor, level)
            if n == quiet_rounds - 1:
                print("Ready! Clap, or play a frog call.\n")
            continue

        if level < floor + LOUDER_THAN_QUIET_BY:
            floor = 0.9 * floor + 0.1 * level  # slowly follow the room's background noise
            bar = "▮" * max(0, min(20, int(level - floor + 10)))
            wait = f"  (new answer in {np.ceil(show_next_after - now):.0f} s)" if holding else " " * 22
            print(f"\r  listening... {bar:<20} {level:3.0f} dB{wait}", end="", flush=True)
            continue

        if holding:                            # still showing the last answer
            continue

        if level < MIN_SOUND_DB:
            print(f"\n  Heard something at {level:.0f} dB, but that's quieter than "
                  f"{MIN_SOUND_DB} dB, so ignoring it.")
            continue

        board_angle, agreement = best_direction(sound, key)
        if agreement < MIN_AGREEMENT:
            print(f"\n  Heard something, but the mic pairs disagree ({agreement:.0%}). "
                  "Echo or noise? Skipping it.")
            continue

        explain(board_angle, agreement, level, floor)
        lights.point(board_angle, bright=True)
        last_angle = board_angle
        show_next_after = now + HOLD_SECONDS


if __name__ == "__main__":
    print(f"Coqui Finder demo  |  board: {BOARD}  |  4 mics, {len(pairs)} mic pairs")
    print("Building the answer key: 360 directions x 6 mic pairs...", end=" ")
    key = build_answer_key()
    print(f"done. The biggest possible gap between two mics is {np.abs(key).max() * 1000:.2f} ms.")
    lights = Lights()
    lights.off()
    try:
        listen(chunks_from_board(), key, lights)
    except KeyboardInterrupt:
        print("\nStopped. Bye!")
    finally:
        lights.off()
