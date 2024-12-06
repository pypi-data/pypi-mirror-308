"""
Card widget for displaying a localized label with a dynamic value.

Each card has a label and a value field, supporting localization and value updates.
"""

import customtkinter as ctk

from letterguesser.gui.frames.BaseFrame import BaseFrame
from letterguesser.styles.font import (
    font,
    text_medium,
    text_medium_height,
    text_small,
    text_small_height
)
from letterguesser.styles.padding import pad_0, pad_2, pad_3


class Card(BaseFrame):
    """Displays a label and a dynamic value."""

    def __init__(
            self,
            parent,
            loc_label_key,
            initial_value,
            var_type='str',
            **kwargs
    ):
        """
        Init a Card.

        :param parent: The parent widget.
        :param loc_label_key: The key of the localization label
        :param initial_value: Initial value of the card
        :param var_type: The type of variable
        :param kwargs: Additional keyword arguments
        """
        super().__init__(parent, **kwargs)

        self.initial_value = initial_value
        self.var_type = var_type

        self.configure(height=70)
        self.propagate(False)

        # var typing shenanigans
        self.var_value = ctk.StringVar(value=initial_value) \
            if var_type == 'str' else ctk.IntVar(value=initial_value)

        self.value = ctk.CTkLabel(
            self,
            textvariable=self.var_value,
            height=text_medium_height,
            anchor='w',
            font=ctk.CTkFont(
                family=font,
                size=text_medium,
                weight='bold'  # sadly, there is no 'semibold' .______.
            )
        )
        self.add_widget(
            self.value,
            side='top',
            expand=False,
            padx=pad_3,
            pady=(pad_3, pad_2)
        )

        # card heading (text that describes what the value is)
        self.label = ctk.CTkLabel(
            self,
            text='',
            anchor='w',
            height=text_small_height,
            font=ctk.CTkFont(
                family=font,
                size=text_small
            )
        )

        self.localisation.bind(self.label, loc_label_key)
        self.add_widget(
            self.label,
            side='top',
            expand=False,
            padx=pad_3,
            pady=(pad_0, pad_3)
        )

    def update_value(self, value: str | int):
        """Update the displayed value on the card."""
        self.var_value.set(value)

    def reset(self):
        """Reset the card value to the initial value."""
        self.update_value(self.initial_value)

    def get_type(self):
        """Get type of the card."""
        return str if isinstance(self.var_value, ctk.StringVar) else int
