"""
OptionMenu widget for a dropdown menu with localization and hover effects.

This widget provides an option menu that supports localization and changes appearance
on hover.
"""

from typing import Any, Callable, Optional

import customtkinter as ctk

from letterguesser.gui.frames.BaseFrame import localisation
from letterguesser.styles.buttons import BUTTON_HEIGHT, BUTTON_WIDTH
from letterguesser.styles.colors import (
    base_fill_1,
    base_surface_1,
    text_primary,
    text_secondary
)


class OptionMenu(ctk.CTkOptionMenu):
    """A dropdown menu with localization, hover effects, and enable/disable states."""

    def __init__(
            self,
            parent: Any,
            label_key: str,
            initial_value: str,
            values: list[str],
            command: Optional[Callable[[str], None]] = None,
            **kwargs: Any
    ) -> None:
        """
        Initialize the OptionMenu with values and localization key.

        :param parent: Parent tkinter widget/frame for the OptionMenu.
        :param label_key: Localization key for the menu label.
        :param initial_value: Initial selected value.
        :param values: List of options available in the menu.
        :param command: Command to execute on selection change.
        :param kwargs: Additional configuration options.
        """
        self.values = values
        self.loc_key = label_key

        self.localisation = localisation
        self.menu_var = ctk.StringVar(value=initial_value)

        super().__init__(
            parent,
            height=BUTTON_HEIGHT,
            width=BUTTON_WIDTH,
            command=command,
            state='normal',
            variable=self.menu_var,
            fg_color=base_surface_1,
            button_color=base_surface_1,
            text_color=text_secondary,
            button_hover_color=base_fill_1,
            values=[],
            **kwargs
        )

        self.bind('<Enter>', self.on_hover)
        self.bind('<Leave>', self.on_leave)
        self.localisation.bind(self, label_key, self.update_loc)

    def disable(self) -> None:
        """Disable the OptionMenu, preventing user interaction."""
        self.configure(state='disabled')

    def enable(self) -> None:
        """Enable the OptionMenu, allowing user interaction."""
        self.configure(state='normal', cursor='hand2')

    def on_hover(self, _event) -> None:
        """Change appearance on hover."""
        if self.cget('state') == 'normal':
            self.configure(
                fg_color=base_fill_1,
                text_color=text_primary,
                button_hover_color=base_fill_1
            )

    def on_leave(self, _event) -> None:
        """Restore appearance when the hover ends."""
        if self.cget('state') == 'normal':
            self.configure(fg_color=base_surface_1, text_color=text_secondary)

    def update_loc(self, text) -> None:
        """
        Update localized text for the OptionMenu items.

        :param text: Localized suffix text for each menu item.
        :return: None
        """
        initial_value = self.menu_var.get().split(' ')[0]
        self.menu_var.set(f'{initial_value} {text}')

        formatted_values = [f'{val} {text}' for val in self.values]
        self.configure(values=formatted_values)
