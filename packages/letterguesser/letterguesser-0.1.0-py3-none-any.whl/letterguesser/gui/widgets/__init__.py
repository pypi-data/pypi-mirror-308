"""
Widgets package for LetterGuesser.

This package provides custom GUI components like buttons, input blocks, and cards,
organized into modular widgets for the application interface.

Available Widgets
-----------------
- `Card`: Displays a localized label and dynamic value.
- `CardGroup`: Manages a group of `Card` widgets.
- `TextBlockSegment`: Displays text content in segments.
- `InputBlock`: Contains input fields with labels and placeholders.
- `Button`: A styled button with localization and state management.
- `ButtonGroup`: Manages a group of `Button` widgets with shared settings.
- `OptionMenu`: A dropdown menu for selecting options.

"""

from .Button import Button
from .ButtonGroup import ButtonGroup
from .Card import Card
from .CardGoup import CardGroup
from .InputBlock import InputBlock
from .OptionMenu import OptionMenu
from .TextBlockSegment import TextBlockSegment

__all__ = [
    'Card',
    'CardGroup',
    'TextBlockSegment',
    'InputBlock',
    'Button',
    'ButtonGroup',
    'OptionMenu'
]
