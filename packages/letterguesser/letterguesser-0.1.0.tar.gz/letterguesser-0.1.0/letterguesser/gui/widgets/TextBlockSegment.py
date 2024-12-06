"""
TextBlockSegment widget for displaying text segments with localization.

This widget shows a labeled text block with localization and updates support.
"""

from typing import Any

import customtkinter as ctk

from letterguesser.gui.frames.BaseFrame import BaseFrame
from letterguesser.styles.font import font, text_small, text_small_height
from letterguesser.styles.padding import pad_0, pad_1


class TextBlockSegment(BaseFrame):
    """A text block widget with localization and automatic updating."""

    def __init__(
            self,
            parent: Any,
            localisation_key: str,
            initial_text: str,
            **kwargs: Any
    ):
        """
        Initialize the TextBlockSegment with initial text and localisation.

        :param parent: The parent widget for the TextBlockSegment.
        :param localisation_key: Localisation key for the label.
        :param initial_text: Initial text to display in the text block.
        :param kwargs: Additional configuration options.
        """
        super().__init__(parent, transparent_bg=True, **kwargs)

        self.text_var = ctk.StringVar(value=initial_text)

        self.label = ctk.CTkLabel(
            self,
            height=text_small_height,
            anchor='w',
            font=ctk.CTkFont(
                family=font,
                size=text_small
            )
        )
        self.localisation.bind(self.label, localisation_key)
        self.add_widget(
            self.label,
            side='top',
            pady=(pad_0, pad_1)
        )

        self.text_block = ctk.CTkEntry(
            self,
            textvariable=self.text_var,
            state='disabled',
            height=40,
            border_width=0
        )
        self.localisation.bind(self.text_block, 'no_input', self.update_value)

        self.add_widget(
            self.text_block,
            side='bottom',
            pady=(pad_1, pad_0)
        )

        self.text_block.configure(
            text_color=ctk.ThemeManager.theme['CTkEntry']['placeholder_text_color'][0]
            )

    def rebind(self, new_loc_key: str) -> None:
        """
        Rebind the text block to a new localization key.

        :param new_loc_key: New localization key to bind to the text block.
        """
        self.localisation.bind(self.text_block, new_loc_key, self.update_value)

    def update_value(self, new_value: str) -> None:
        """
        Update the displayed text in the text block.

        :param new_value: New text to display in the text block.
        """
        self.text_var.set(new_value)

    def reset(self) -> None:
        """Reset the text block to the initial localization key."""
        self.localisation.bind(self.text_block, 'no_input', self.update_value)
