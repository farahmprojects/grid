"""
TP2 - Exercise 1 - Graphical interface (GIVEN - you do not need to modify it)
=============================================================================

Run it with:  python3 grid_gui.py

This file only takes care of the display: it draws the 4 x 4 grid and the
character, listens to the mouse, and animates the moves. Every decision
(which cell was clicked, is the move allowed, which path to follow) is taken
by the functions YOU write in moves.py.

If a function of moves.py is not written yet, the window does not crash: the
message is shown in the status bar at the bottom.
"""

import os
import traceback
import tkinter as tk

import moves

CELL = 110                      # size of a cell, in pixels
SIZE = moves.GRID_SIZE          # number of cells per side (4)
START = (0, 0)                  # starting cell of the character
WALLS = {(1, 0), (2, 2)}        # walls used in the "walls" mode
STEP_DELAY = 180                # milliseconds between two animated steps

IMAGE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "character.png")

COLOURS = {
    "light": "#f4f1ea",
    "dark": "#e7e1d3",
    "grid": "#b9b09c",
    "wall": "#5b5246",
    "target": "#9bc53d",
    "refused": "#d64545",
    "text": "#8a8170",
}

MODES = [
    ("Jump", "jump"),
    ("Neighbour only", "neighbour"),
    ("Walk", "walk"),
    ("Walk with walls", "walls"),
]


class GridApp:
    """The window. It keeps the position of the character and calls moves.py."""

    def __init__(self, root):
        self.root = root
        root.title("TP2 - Move the character")
        root.resizable(False, False)

        self.position = START
        self.steps = 0              # total number of cells walked
        self.animating = False

        # --- top bar: the mode -------------------------------------------
        top = tk.Frame(root, padx=10, pady=8)
        top.pack(fill="x")
        tk.Label(top, text="Mode:", font=("Helvetica", 11, "bold")).pack(side="left")
        self.mode = tk.StringVar(value="jump")
        for label, value in MODES:
            tk.Radiobutton(top, text=label, value=value, variable=self.mode,
                           command=self.redraw).pack(side="left", padx=4)

        # --- the grid ----------------------------------------------------
        self.canvas = tk.Canvas(root, width=SIZE * CELL, height=SIZE * CELL,
                                highlightthickness=0, bg=COLOURS["light"])
        self.canvas.pack(padx=10)
        self.canvas.bind("<Button-1>", self.on_click)

        # --- bottom bar: status and reset --------------------------------
        bottom = tk.Frame(root, padx=10, pady=8)
        bottom.pack(fill="x")
        self.info = tk.Label(bottom, anchor="w", font=("Helvetica", 11))
        self.info.pack(side="left")
        tk.Button(bottom, text="Reset", command=self.reset).pack(side="right")
        self.status = tk.Label(root, anchor="w", padx=10, pady=4,
                               font=("Helvetica", 10), fg="#444")
        self.status.pack(fill="x")

        self.image = self.load_image()
        self.redraw()
        self.say("Click on a cell to move the character.")

    # ------------------------------------------------------------------ images
    def load_image(self):
        """Load character.png and shrink it so that it fits in a cell."""
        try:
            img = tk.PhotoImage(file=IMAGE_FILE)
        except tk.TclError:
            return None                     # no picture: a circle is drawn instead
        biggest = max(img.width(), img.height())
        factor = 1
        while biggest / factor > CELL * 0.8:
            factor += 1
        return img.subsample(factor) if factor > 1 else img

    # ----------------------------------------------------------------- drawing
    def current_walls(self):
        return WALLS if self.mode.get() == "walls" else set()

    def cell_box(self, cell):
        row, col = cell
        return col * CELL, row * CELL, (col + 1) * CELL, (row + 1) * CELL

    def redraw(self, highlight=None, colour=None):
        c = self.canvas
        c.delete("all")
        walls = self.current_walls()
        for row in range(SIZE):
            for col in range(SIZE):
                x0, y0, x1, y1 = self.cell_box((row, col))
                fill = COLOURS["light"] if (row + col) % 2 == 0 else COLOURS["dark"]
                if (row, col) in walls:
                    fill = COLOURS["wall"]
                c.create_rectangle(x0, y0, x1, y1, fill=fill, outline=COLOURS["grid"])
                c.create_text(x0 + 6, y0 + 4, anchor="nw", text=f"({row},{col})",
                              fill=COLOURS["text"], font=("Courier", 9))
        if highlight is not None:
            x0, y0, x1, y1 = self.cell_box(highlight)
            c.create_rectangle(x0 + 3, y0 + 3, x1 - 3, y1 - 3,
                               outline=colour, width=4)
        self.draw_character()
        self.info.config(text=f"Position: {self.position}    Steps walked: {self.steps}")

    def draw_character(self):
        x0, y0, x1, y1 = self.cell_box(self.position)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        if self.image is not None:
            self.canvas.create_image(cx, cy, image=self.image)
        else:
            r = CELL * 0.3
            self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                                    fill="#e05a47", outline="")

    def say(self, text, error=False):
        self.status.config(text=text, fg="#b02a2a" if error else "#444")

    # ------------------------------------------------------- calling moves.py
    def call_student(self, function, *args):
        """Call a function of moves.py; return (ok, result)."""
        try:
            return True, function(*args)
        except NotImplementedError as err:
            self.say(f"moves.py: the function {err} is not written yet.", error=True)
        except Exception as err:                      # show the bug, do not crash
            traceback.print_exc()
            self.say(f"moves.py: {function.__name__} raised "
                     f"{type(err).__name__}: {err}", error=True)
        return False, None

    def on_click(self, event):
        if self.animating:
            return
        ok, target = self.call_student(moves.pixel_to_cell, event.x, event.y, CELL)
        if not ok:
            return
        if not (isinstance(target, tuple) and len(target) == 2):
            self.say(f"pixel_to_cell must return a tuple (row, col), got {target!r}", error=True)
            return

        mode = self.mode.get()
        ok, path = self.call_student(moves.move, self.position, target, mode,
                                     frozenset(self.current_walls()))
        if not ok:
            return
        if not isinstance(path, list):
            self.say(f"move must return a list, got {path!r}", error=True)
            return
        if not path:
            self.redraw(highlight=target, colour=COLOURS["refused"])
            self.say(f"Move to {target} refused in mode '{mode}'.")
            return
        bad = [cell for cell in path
               if not (isinstance(cell, tuple) and len(cell) == 2
                       and 0 <= cell[0] < SIZE and 0 <= cell[1] < SIZE)]
        if bad:
            self.say(f"move returned cells outside the grid: {bad}", error=True)
            return
        self.say(f"Path to {target}: {path}")
        self.animate(path, target)

    def animate(self, path, target):
        """Move the character one cell of the path at a time."""
        if not path:
            self.animating = False
            return
        self.animating = True
        self.position = path[0]
        self.steps += 1
        self.redraw(highlight=target, colour=COLOURS["target"])
        self.root.after(STEP_DELAY, self.animate, path[1:], target)

    def reset(self):
        if self.animating:
            return
        self.position = START
        self.steps = 0
        self.redraw()
        self.say("Back to the start.")


if __name__ == "__main__":
    root = tk.Tk()
    GridApp(root)
    root.mainloop()
