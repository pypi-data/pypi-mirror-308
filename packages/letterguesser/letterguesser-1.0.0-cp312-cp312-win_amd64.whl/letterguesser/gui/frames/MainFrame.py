"""
MainFrame to display left and right frames in main layout.

Contains LeftFrame and RightFrame to manage main application layout.
"""

from letterguesser.styles.padding import pad_0, pad_4

from .BaseFrame import BaseFrame
from .LeftFrame import LeftFrame
from .RightFrame import RightFrame


class MainFrame(BaseFrame):
    """
    Main application frame organizing left and right frames.

    Provides the main layout structure, dividing the app into left and right frames.
    """

    def __init__(self, parent, **kwargs):
        """
        Initialize MainFrame with left and right frames.

        :param parent: The parent tkinter object.
        :param kwargs: Additional keyword arguments for frame configuration.
        """
        super().__init__(parent, transparent_bg=True, **kwargs)

        self.left_frame = LeftFrame(self)
        self.add_widget(
            self.left_frame,
            side='left',
            fill='both',
            expand=True,
            padx=(pad_0, pad_4)
        )

        self.right_frame = RightFrame(self)
        self.add_widget(
            self.right_frame,
            side='right',
            fill='both',
            expand=True,
            padx=(pad_4, pad_0)
        )
