"""
LetterGuesser - Entry point.

This script allows you to run LetterGuesser as a standalone application from the
command line. Executing this module will launch CustomTkinter GUI app.

Usage:
------
To run this script, use the following command:

    python -m letterguesser

Options:
--------
No options supported
"""

import customtkinter as ctk

from letterguesser.config import APP_SIZE, APP_TITLE
from letterguesser.context import localisation, manager
from letterguesser.gui.frames import HeaderFrame, MainFrame
from letterguesser.styles.padding import pad_0, pad_6


class App(ctk.CTk):
    """Represent the main application interface."""

    def __init__(self):
        """Initialize an instance of the App class."""
        # windows setup
        super().__init__()
        self.title(APP_TITLE)

        # from context set global localisation instance
        self.localisation = localisation
        self.manager = manager

        # offsets to run app in the center of the screen
        # host display width x height
        display = (self.winfo_screenwidth(), self.winfo_screenheight())
        left = int(display[0] / 2 - APP_SIZE[0] / 2)
        top = int(display[1] / 2 - APP_SIZE[1] / 2)
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}+{left}+{top}')

        # windows constraints
        # precautions, if resizable(false, false) fails
        self.minsize(APP_SIZE[0], APP_SIZE[1])
        self.maxsize(APP_SIZE[0], APP_SIZE[1])
        self.resizable(False, False)

        # main layout
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.header_frame = HeaderFrame(self)
        self.header_frame.grid(
            row=0,
            column=0,
            sticky='nsew',
            padx=pad_6,
            pady=pad_6
        )

        self.main_frame = MainFrame(self)
        self.main_frame.grid(
            row=1,
            column=0,
            sticky='nsew',
            padx=pad_6,
            pady=(pad_0, pad_6)
        )

        # key binds
        self.bind('<Escape>', lambda event: self.quit())
        self.bind('<Control-l>', lambda event: self.header_frame.toggle_langauge())

        # run app
        self.mainloop()


if __name__ == "__main__":
    App()
# end main
