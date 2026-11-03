"""
coqui_live.py - a live picture of which way the sound is coming from.

It uses all the settings and maths from coqui_demo.py (keep both files in the
same folder), so your calibration (ZERO_DEGREES, CLOCKWISE, FULL_SCALE_DB, the
LED settings...) only needs to be changed there.

What you see:
  * A compass with angles running clockwise. 0° is on the right by default; change
    ZERO_AT below to put it at the top ("N"), bottom ("S") or left ("W").
  * A red arrow pointing at the direction of the latest sound.
  * Orange dots around the edge for recent sounds (they fade as they get older),
    so you can see whether the sounds keep coming from the same place.
  * A big angle number, and a level bar at the bottom showing how much louder
    the sound is than the quiet room (the black line is the "loud enough" mark).

To run it (in a terminal, in the folder with both files):

    python3 -m pip install numpy sounddevice pyusb matplotlib
    python3 coqui_live.py

Close the window (or press Ctrl+C in the terminal) to stop.
"""
import threading
import time
import textwrap
from collections import deque

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import coqui_demo as cd

# =============================================================================
# SETTINGS FOR THE PICTURE
# =============================================================================
HOLD_SECONDS = 1.0     # after showing an answer, wait this long before the next one
                       # (the demo uses 5 s; shorter looks better on a live picture)
TRAIL_SECONDS = 20     # recent sounds stay on the edge of the compass this long
FADE_SECONDS = 6       # the red arrow fades to pale over this long
MAX_BAR_DB = 40        # the level bar is this many dB wide
QUIET_ROUNDS = 4       # how many chunks we listen to, to learn the quiet room
READY_TEXT = "Listening... clap or play a frog call"
ZERO_AT = "E"          # where 0° is drawn on the compass: "N" = top, "E" = right,
                       # "S" = bottom, "W" = left. Angles still run clockwise.
                       # This only turns the picture; it doesn't change the angles.
PANEL_WIDTH = 56       # how many characters wide the text panel on the right is
ORDINALS = ["1st", "2nd", "3rd", "4th"]
RANK_COLOURS = ["#4caf50", "#a5d66f", "#ffd966", "#f08a7e"]   # first = green ... last = red
PRINT_TEXT_COMPASS = False   # also print the little text compass from coqui_demo.py
                             # (it always has 0° at the top, so it won't match the picture)


# =============================================================================
# SHARED NOTEBOOK: the listening thread writes, the picture reads
# =============================================================================
class State:
    def __init__(self):
        self.lock = threading.Lock()
        self.status = "Starting..."
        self.level = 0.0
        self.floor = None
        self.error = None
        self.explanation = ""                  # the step-by-step text for the side panel
        self.mic_ms = None                     # ms after the first mic, for mics A, B, C, D
        self.detections = deque(maxlen=300)    # (time, chalk angle, agreement, level)

    def set(self, **values):
        with self.lock:
            for name, value in values.items():
                setattr(self, name, value)

    def add_detection(self, chalk_angle, agreement, level):
        with self.lock:
            self.detections.append((time.time(), chalk_angle, agreement, level))

    def snapshot(self):
        with self.lock:
            return {"status": self.status, "level": self.level, "floor": self.floor,
                    "error": self.error, "explanation": self.explanation,
                    "mic_ms": self.mic_ms,
                    "detections": list(self.detections)}


# =============================================================================
# THE LISTENING THREAD (same steps as coqui_demo.listen, but it feeds the picture)
# =============================================================================
def explanation_lines(board_angle, agreement, level, floor):
    """The same step-by-step lines as coqui_demo.py's printout."""
    chalk_angle = cd.to_chalk(board_angle)
    t = cd.arrival_times(board_angle)
    order = np.argsort(t)
    lines = [
        f"  Heard something!  {level:.0f} dB at the board "
        f"({level - floor:.0f} dB louder than the quiet room)",
        "  Graded it against all 360 directions in the answer key.",
        f"  Best match: {chalk_angle}°   (board angle {board_angle}°, "
        f"the 6 mic pairs agree {agreement:.0%})",
        "  That direction means the sound reached the mics in this order:",
    ]
    for rank, m in enumerate(order):
        lines.append(f"     {rank + 1}. mic {cd.MIC_NAMES[m]}   +{(t[m] - t[order[0]]) * 1000:.2f} ms")
    return lines


def print_explanation(lines, board_angle):
    """Show the lines in the terminal, exactly like coqui_demo.py."""
    print("\n")
    for line in lines:
        print(line)
    if PRINT_TEXT_COMPASS:
        print(cd.draw_compass(cd.to_chalk(board_angle)))


def panel_text(lines):
    """The same lines, wrapped to fit the side panel of the window."""
    out = []
    for line in lines:
        text = line.strip()
        indent = "   " if text[:1].isdigit() else ""        # the mic order list
        out.append(textwrap.fill(text, PANEL_WIDTH, initial_indent=indent,
                                 subsequent_indent=indent + "   "))
    return "\n".join(out)


def mic_delays_ms(board_angle):
    """How many milliseconds after the first mic each mic (A, B, C, D) hears the sound."""
    t = cd.arrival_times(board_angle)
    return [float(x) for x in (t - t.min()) * 1000]


def board_to_display(board_deg):
    """The same turn as cd.to_chalk, but without rounding (used to place the mics)."""
    turned = board_deg - cd.ZERO_DEGREES
    return (-turned if cd.CLOCKWISE else turned) % 360


def audio_worker(state, key, lights, stop):
    channels = cd.BOARDS[cd.BOARD]["channels"]
    chunks = None
    try:
        chunks = cd.chunks_from_board()
        floor = None
        show_next_after = 0.0
        last_angle = None
        note_until = 0.0              # keep a short message on screen until this time
        state.set(status="Measuring the quiet room... please stay quiet")
        for n, chunk in enumerate(chunks):
            if stop.is_set():
                break
            now = n * cd.CHUNK_SECONDS
            holding = now < show_next_after
            if not holding and last_angle is not None:
                lights.point(last_angle, bright=False)    # dim the light, ready for a new answer
                last_angle = None
            sound = chunk[:, channels]
            level = cd.loudness_db(sound)

            if n < QUIET_ROUNDS:                          # learning what "quiet" sounds like
                floor = level if floor is None else min(floor, level)
                state.set(level=level, floor=floor)
                if n == QUIET_ROUNDS - 1:
                    state.set(status=READY_TEXT)
                continue

            if level < floor + cd.LOUDER_THAN_QUIET_BY:
                floor = 0.9 * floor + 0.1 * level         # slowly follow the background noise
                state.set(level=level, floor=floor)
                if time.time() > note_until:
                    state.set(status=READY_TEXT)
                continue

            state.set(level=level, floor=floor)
            if holding:
                continue

            if level < cd.MIN_SOUND_DB:
                state.set(status=f"Heard something at {level:.0f} dB, quieter than "
                                 f"{cd.MIN_SOUND_DB} dB, so ignored")
                note_until = time.time() + 2
                continue

            board_angle, agreement = cd.best_direction(sound, key)
            if agreement < cd.MIN_AGREEMENT:
                state.set(status=f"Mic pairs disagree ({agreement:.0%}): echo or noise? Skipped")
                note_until = time.time() + 2
                continue

            chalk = cd.to_chalk(board_angle)
            state.add_detection(chalk, agreement, level)
            state.set(status=READY_TEXT)
            lines = explanation_lines(board_angle, agreement, level, floor)
            state.set(explanation=panel_text(lines), mic_ms=mic_delays_ms(board_angle))
            print_explanation(lines, board_angle)
            lights.point(board_angle, bright=True)
            last_angle = board_angle
            show_next_after = now + HOLD_SECONDS
    except SystemExit as e:                               # e.g. board not found
        state.set(error=str(e.code))
        print(f"\n{e.code}")
    except Exception as e:
        state.set(error=f"{type(e).__name__}: {e}")
        print(f"\nListening stopped: {type(e).__name__}: {e}")
    finally:
        if chunks is not None:
            chunks.close()


# =============================================================================
# THE PICTURE
# =============================================================================
def build_figure(state):
    fig = plt.figure(figsize=(12, 8))
    try:
        fig.canvas.manager.set_window_title("Coqui Finder - live")
    except Exception:
        pass

    # The compass: angles going clockwise, with 0° wherever ZERO_AT says.
    ax = fig.add_axes([0.03, 0.21, 0.55, 0.63], projection="polar")
    ax.set_theta_zero_location(ZERO_AT)
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 1.05)
    ax.set_rticks([])
    ax.set_thetagrids(range(0, 360, 30), labels=[f"{a}°" for a in range(0, 360, 30)])
    ax.grid(True, alpha=0.4)
    ax.plot([0], [0], "o", color="black", markersize=14, zorder=5)    # the board

    trail = ax.scatter([], [], s=140, zorder=3)
    trail.set_edgecolor("none")
    arrow, = ax.plot([], [], lw=5, color="red", marker="o", markersize=16,
                     markevery=[1], zorder=4, solid_capstyle="round")

    big = fig.text(0.305, 0.945, "--", ha="center", va="center", fontsize=34, weight="bold")
    detail = fig.text(0.305, 0.895, "", ha="center", va="center", fontsize=11, color="dimgray")
    status = fig.text(0.305, 0.145, "", ha="center", va="center", fontsize=11)

    # The side panel: the step-by-step explanation of the latest sound.
    fig.text(0.60, 0.90, "How the last sound was worked out", ha="left", va="center",
             fontsize=13, weight="bold")
    panel = fig.text(0.60, 0.855, "", ha="left", va="top", fontsize=9, family="monospace",
                     linespacing=1.35)

    # The level bar along the bottom.
    ax2 = fig.add_axes([0.06, 0.085, 0.49, 0.035])
    ax2.set_xlim(0, MAX_BAR_DB)
    ax2.set_ylim(0, 1)
    ax2.set_yticks([])
    ax2.set_xlabel("dB louder than the quiet room", fontsize=9)
    ax2.axvline(cd.LOUDER_THAN_QUIET_BY, color="black", lw=2)
    bar = ax2.barh([0.5], [0], height=0.8, color="tab:gray")[0]

    # Which mic heard it first: the 4 mics drawn on the board, turned the same way as the compass.
    fig.text(0.79, 0.585, "Which mic heard it first", ha="center", va="center",
             fontsize=13, weight="bold")
    axm = fig.add_axes([0.64, 0.15, 0.30, 0.42], projection="polar")
    axm.set_theta_zero_location(ZERO_AT)
    axm.set_theta_direction(-1)
    axm.set_ylim(0, 1.3)
    axm.set_axis_off()
    ring = np.linspace(0, 2 * np.pi, 200)
    axm.fill(ring, np.full(200, 0.95), color="#eeeeee", zorder=0)           # the board
    axm.plot(ring, np.full(200, 0.95), color="gray", lw=1, zorder=1)
    mic_theta = np.radians([board_to_display(np.degrees(np.arctan2(y, x))) for x, y in cd.mics])
    MIC_R = 0.58
    mic_dots = axm.scatter(mic_theta, np.full(4, MIC_R), s=3000, c=["lightgray"] * 4,
                           edgecolors="black", linewidths=1.5, zorder=3)
    mic_texts = [axm.text(mic_theta[k], MIC_R, cd.MIC_NAMES[k], ha="center", va="center",
                          fontsize=9.5, zorder=4) for k in range(4)]
    sound_arrow = axm.annotate("", xy=(0, 1.0), xytext=(0, 1.3), annotation_clip=False,
                               arrowprops=dict(arrowstyle="-|>", color="red", lw=3,
                                               mutation_scale=22))
    sound_arrow.set_visible(False)
    fig.text(0.79, 0.105, "green = heard it first, red = heard it last\n"
             "red arrow = where the sound came from", ha="center", va="center",
             fontsize=9, color="dimgray")

    def update(_frame):
        s = state.snapshot()
        now = time.time()
        recent = [d for d in s["detections"] if now - d[0] <= TRAIL_SECONDS]

        if recent:
            t, angle, agreement, level = recent[-1]
            age = now - t
            theta = np.radians(angle)
            arrow.set_data([theta, theta], [0, 0.88])
            arrow.set_alpha(max(0.25, 1 - age / FADE_SECONDS))
            big.set_text(f"{angle}°")
            detail.set_text(f"{level:.0f} dB   mic pairs agree {agreement:.0%}   {age:.0f} s ago")

            ages = np.array([now - d[0] for d in recent])
            thetas = np.radians([d[1] for d in recent])
            trail.set_offsets(np.column_stack([thetas, np.full(len(recent), 1.0)]))
            colours = np.zeros((len(recent), 4))
            colours[:, 0], colours[:, 1], colours[:, 2] = 1.0, 0.55, 0.0      # orange
            colours[:, 3] = np.clip(1 - ages / TRAIL_SECONDS, 0.08, 0.9)
            trail.set_facecolors(colours)
        else:
            arrow.set_data([], [])
            big.set_text("--")
            detail.set_text("no sound heard yet")
            trail.set_offsets(np.empty((0, 2)))

        panel.set_text(s["explanation"] or "Waiting for a sound...")

        ms = s["mic_ms"]
        if recent and ms is not None:
            order = np.argsort(ms)                       # mic numbers, earliest first
            rank = np.empty(4, dtype=int)
            rank[order] = np.arange(4)
            mic_dots.set_facecolors([RANK_COLOURS[r] for r in rank])
            for k in range(4):
                mic_texts[k].set_text(f"{cd.MIC_NAMES[k]}\n{ORDINALS[rank[k]]}\n+{ms[k]:.2f} ms")
            th = np.radians(recent[-1][1])
            sound_arrow.xy = (th, 1.0)
            sound_arrow.xyann = (th, 1.3)
            sound_arrow.set_visible(True)
        else:
            mic_dots.set_facecolors(["lightgray"] * 4)
            for k in range(4):
                mic_texts[k].set_text(cd.MIC_NAMES[k])
            sound_arrow.set_visible(False)

        floor = s["floor"]
        over = 0.0 if floor is None else max(0.0, s["level"] - floor)
        bar.set_width(min(over, MAX_BAR_DB))
        bar.set_color("tab:orange" if over >= cd.LOUDER_THAN_QUIET_BY else "tab:gray")

        if s["error"]:
            status.set_text("\n".join(textwrap.wrap(s["error"], 70)))
            status.set_color("red")
        else:
            status.set_text(s["status"])
            status.set_color("black")

    return fig, update


# =============================================================================
# START EVERYTHING
# =============================================================================
def main():
    print(f"Coqui Finder (live picture)  |  board: {cd.BOARD}")
    print("Building the answer key...", end=" ")
    key = cd.build_answer_key()
    print("done.")
    lights = cd.Lights()
    lights.off()

    state = State()
    stop = threading.Event()
    worker = threading.Thread(target=audio_worker, args=(state, key, lights, stop), daemon=True)
    worker.start()

    fig, update = build_figure(state)
    fig.canvas.mpl_connect("close_event", lambda event: stop.set())
    animation = FuncAnimation(fig, update, interval=100, cache_frame_data=False)  # noqa: F841
    try:
        plt.show()
    except KeyboardInterrupt:
        pass
    finally:
        stop.set()
        worker.join(timeout=2)
        lights.off()
        print("\nStopped. Bye!")


if __name__ == "__main__":
    main()
