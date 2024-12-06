"""Scrollable version of BaseFrame."""

import customtkinter as ctk

from letterguesser.context import localisation, manager
from letterguesser.styles.colors import text_secondary
from letterguesser.styles.font import (
    font,
    text_small,
    text_small_height
)
from letterguesser.styles.padding import pad_2, pad_3


class BaseScrollFrame(ctk.CTkScrollableFrame):
    """
    Scrollable frame with title, transparency, and access to core app instances.

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
        Initialize BaseScrollFrame with title and transparency options.

        :param parent: Parent tkinter object for the frame.
        :param title_key: Localisation key for the title.
        :param transparent_bg: Enables transparent background if True.
        """
        super().__init__(parent, **kwargs)

        if transparent_bg:
            self.configure(fg_color='transparent')

        # connect to the global localisation instance
        self.localisation = localisation
        self.manager = manager

        self.title_label = None
        if title_key:
            self.title_label = ctk.CTkLabel(
                self,
                height=text_small_height,
                font=ctk.CTkFont(
                    family=font,
                    size=text_small
                )
            )
            self.localisation.bind(self.title_label, title_key)
            self.title_label.pack(
                side='top',
                expand=False,
                anchor='w',
                padx=pad_3,
                pady=(pad_3, pad_2)
            )

        self.placeholder: ctk.CTkLabel | None = None

    def set_placeholder(self, text_key):
        """
        Set placeholder text with localisation binding.

        :param text_key: Localisation key for placeholder text.
        """
        if not self.placeholder:
            self.placeholder = ctk.CTkLabel(
                self,
                text_color=text_secondary,
                height=text_small,
                font=ctk.CTkFont(
                    family=font,
                    size=text_small
                )
            )

        self.localisation.bind(self.placeholder, text_key)

    def show_placeholder(self):
        """Display the placeholder text in the frame."""
        if self.placeholder:
            self.placeholder.pack(pady=(100, 0), expand=True)

    def hide_placeholder(self):
        """Hide the placeholder text from the frame."""
        if self.placeholder:
            self.placeholder.pack_forget()
