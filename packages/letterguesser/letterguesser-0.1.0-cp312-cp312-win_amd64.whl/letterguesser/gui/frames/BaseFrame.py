"""
BaseFrame provides a custom frame with optional title and transparency.

BaseFrame is a reusable frame that includes support for a title and optional
transparency, serving as a foundational frame for other frames. It also
provides access to core application instances, such as localisation,
experiment manager, and logger, which are passed through this frame for
consistent use across the application.
"""

import customtkinter as ctk

from letterguesser.context import localisation, logger, manager
from letterguesser.styles.padding import pad_4


class BaseFrame(ctk.CTkFrame):
    """
    Custom frame with title, transparency, and access to core app instances.

    BaseFrame allows child frames to inherit standard UI properties and access
    key application instances (`localisation`, `manager`, `logger`), ensuring
    consistent settings and centralized configuration.
    """

    def __init__(
            self,
            parent,
            title_key=None,
            transparent_bg=False,
            **kwargs
    ):
        """
        Initialize BaseFrame with title, transparency, and core instances.

        :param parent: Parent tkinter object for the frame.
        :param title_key: Localisation key for the frame title.
        :param transparent_bg: Enables transparent background if True.
        """
        super().__init__(parent, **kwargs)

        if transparent_bg:
            self.configure(fg_color='transparent')

        # connect to the global localisation instance
        self.localisation = localisation
        self.manager = manager
        self.log = logger

        self.title_label = None
        if title_key:
            self.title_label = ctk.CTkLabel(self, text='')
            self.localisation.bind(self.title_label, title_key)
            self.title_label.pack(side='top', anchor='w', padx=pad_4, pady=pad_4)

    def add_widget(
            self,
            widget,
            side: str = 'top',
            fill: str | None = 'both',
            expand: bool = True,
            anchor: str = 'w',
            padx: int | tuple[int, int] = 0,
            pady: int | tuple[int, int] = 0
    ) -> None:
        """
        Add a widget to the frame with specified packing options.

        :param widget: Widget to add to the frame.
        :param side: Packing side.
        :param fill: Fill direction.
        :param expand: Allow expansion.
        :param anchor: Anchor alignment.
        :param padx: Horizontal padding.
        :param pady: Vertical padding.
        """
        widget.pack(
            side=side,
            fill=fill,
            expand=expand,
            anchor=anchor,
            padx=padx,
            pady=pady
        )


__all__ = ['BaseFrame', 'localisation']
