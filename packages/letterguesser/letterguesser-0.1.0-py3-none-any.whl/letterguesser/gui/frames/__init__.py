"""
Frames package for LetterGuesser application.

Available Frames
----------------
- `AttemptsList`: Displays a list of attempted characters.
- `BaseFrame`: Base frame with support for title and transparency.
- `BaseScrollFrame`: Scrollable frame with optional title and placeholder.
- `BaseTable`: Base frame for displaying tabular data with placeholders.
- `HeaderFrame`: Displays the app title and allows language selection.
- `InputFrame`: Holds user input fields and action buttons.
- `LeftFrame`: Contains cards, input, and status display areas.
- `MainFrame`: Organizes the main layout with left and right frames.
- `ProbabilityTable`: Table for displaying attempt probabilities.
- `RightFrame`: Holds probability and attempt tables.
- `StatusFrame`: Displays current status messages to the user.

Usage
-----
Import any frame from the `frames` package to integrate it into the application:

    from letterguesser.gui.frames import MainFrame, LeftFrame, RightFrame

    main_frame = MainFrame(parent)
"""

from .AttemptsList import AttemptsList
from .HeaderFrame import HeaderFrame
from .InputFrame import InputFrame
from .LeftFrame import LeftFrame
from .MainFrame import MainFrame
from .ProbabilityTable import ProbabilityTable
from .RightFrame import RightFrame
from .StatusFrame import StatusFrame

__all__ = [
    'HeaderFrame',
    'MainFrame',
    'InputFrame',
    'RightFrame',
    'LeftFrame',
    'StatusFrame',
    'ProbabilityTable',
    'AttemptsList'
]
