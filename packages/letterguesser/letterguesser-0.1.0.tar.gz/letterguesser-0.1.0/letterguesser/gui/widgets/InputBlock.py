"""
InputBlock widget with a label and entry field.

This block provides an input field with a localized label and optional placeholder.
"""

from typing import Any

import customtkinter as ctk

from letterguesser.gui.frames.BaseFrame import BaseFrame
from letterguesser.styles.font import font, text_small, text_small_height
from letterguesser.styles.padding import pad_0, pad_1


class InputBlock(BaseFrame):
    """Input block with a label and entry field."""

    def __init__(
            self,
            parent,
            loc_label_key,
            loc_placeholder_key,
            is_disabled=False,
            **kwargs
    ):
        """
        Init InputBlock.

        :param parent: The parent widget.
        :param loc_label_key: Localisation key for the label.
        :param loc_placeholder_key: Localisation key for the placeholder.
        :param is_disabled: Whether the widget is disabled.
        :param kwargs: Additional keywords.
        """
        super().__init__(parent, transparent_bg=True, **kwargs)

        self.input_var = ctk.StringVar(value='')
        self.placeholder = loc_placeholder_key

        # label for the input
        self.label = ctk.CTkLabel(
            self,
            height=text_small_height,
            anchor='w',
            font=ctk.CTkFont(
                family=font,
                size=text_small
            )
        )

        self.localisation.bind(self.label, loc_label_key)
        self.add_widget(
            self.label,
            side='top',
            pady=(pad_0, pad_1)
        )

        self.input_field = ctk.CTkEntry(
            self,
            textvariable=self.input_var,
            height=40,
            font=ctk.CTkFont(
                family=font,
                size=text_small
            )
        )

        self.localisation.bind(self.input_field, loc_placeholder_key, self.update_input)
        self.add_widget(
            self.input_field,
            side='top',
            pady=(pad_1, pad_0)
        )

        if is_disabled:
            self.disable()

        self.input_field.bind('<Return>', self.input_handler)

    def reset(self):
        """Reset input block to default state."""
        self.localisation.bind(self.input_field, self.placeholder, self.update_input)

    def input_handler(self, _event) -> None:
        """Handle input events and forward the input to the manager."""
        self.manager.input_handler(self.get_input())

    def get_input(self) -> Any:
        """Return the current input value."""
        return self.input_var.get()

    def clear(self) -> None:
        """Clear the input field content."""
        self.input_var.set('')

    def update_input(self, new_value: str) -> None:
        """
        Update the input field with a new value.

        :param new_value: The value to set in the input field.
        :return: None
        """
        self.input_var.set(new_value)

    def enable(self):
        """Enable the input field for user entry."""
        self.input_field.configure(state='normal')
        self.input_field.configure(
            text_color=ctk.ThemeManager.theme['CTkEntry']['text_color']
        )

    def disable(self):
        """Disable the input field to prevent interaction."""
        self.input_field.configure(state='disabled')
        self.input_field.configure(
            text_color=ctk.ThemeManager.theme['CTkEntry']['placeholder_text_color']
        )
