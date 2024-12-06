"""
ListItem widget for displaying individual data entries in a list.

Each item displays data with optional alternating row colors.
"""

import customtkinter as ctk

from letterguesser.gui.frames.BaseFrame import BaseFrame
from letterguesser.styles.font import (
    font,
    text_small,
    text_small_height
)
from letterguesser.styles.padding import pad_0, pad_2


class ListItem(BaseFrame):
    """A list item to display structured data."""

    def __init__(
            self,
            parent,
            data,
            is_odd=False,
            **kwargs
    ):
        """
        List item to display data in the structured format.

        :param parent: Parent widget.
        :param data: A dict or tuple containing data to display
        :param is_odd: Determines the background (for row alternating)
        """
        super().__init__(parent, **kwargs)

        self.data = data

        color1 = ctk.ThemeManager.theme["CTk"]["fg_color"]
        color2 = ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"]

        fg_color = color2 if is_odd else color1
        self.configure(fg_color=fg_color)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure((0, 1), weight=1)

        leading_key = self.data['leading'].get('key', None)
        leading_value = self.data['leading'].get('value', None)

        self.leading = ctk.CTkLabel(
            self,
            height=text_small_height,
            font=ctk.CTkFont(
                family=font,
                size=text_small
            )
        )
        self.localisation.bind(
            self.leading,
            leading_key,
            lambda text: self.update_leading(text, leading_value)
        )
        self.leading.grid(row=0, column=0, sticky='w', padx=pad_2, pady=(pad_2, pad_0))

        trailing_key = self.data['trailing'].get('key', None)
        trailing_value = self.data['trailing'].get('value', None)
        self.trailing = ctk.CTkLabel(
            self,
            height=text_small_height,
            font=ctk.CTkFont(
                family=font,
                size=text_small
            )
        )
        self.localisation.bind(
            self.trailing,
            trailing_key,
            lambda text: self.update_trailing(text, trailing_value)
        )
        self.trailing.grid(row=0, column=1, sticky='w', pady=(pad_2, pad_0))

        sub_value = self.data['sub'].get('value', None)
        self.sub = ctk.CTkLabel(
            self,
            text=sub_value,
            font=ctk.CTkFont(
                family=font,
                size=text_small
            )
        )
        self.sub.grid(row=1, column=0, columnspan=2, sticky='w', padx=pad_2,
                      pady=(pad_0, pad_2)
                      )

    def update_leading(self, text: str, value: str) -> None:
        """
        Update the leading label text.

        :param text: The leading label text.
        :param value: The corresponding value for the label.
        :return: None
        """
        self.leading.configure(text=f"{text}: {value}")

    def update_trailing(self, text: str, value: str) -> None:
        """
        Update the trailing label text.

        :param text: The trailing label text.
        :param value: The corresponding value for the label.
        :return: None
        """
        self.trailing.configure(text=f"{text}: {value}")

    def update_sub(self, value: str) -> None:
        """
        Update the sub label text.

        :param value: The subtext value to update.
        :return: None
        """
        self.sub.configure(text=value)
