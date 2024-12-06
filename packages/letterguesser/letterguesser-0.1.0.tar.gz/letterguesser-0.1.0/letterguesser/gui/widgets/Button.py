"""
Button widget with customizable styles and localization support.

This widget provides a styled button with various configurations (e.g., default,
primary, danger) and supports localization for its label.
"""

from typing import Callable, Dict, Optional, Tuple, TypedDict

import customtkinter as ctk

import letterguesser.styles.buttons as buttons
from letterguesser.gui.frames.BaseFrame import localisation


class ColorState(TypedDict):
    """Represents the color state for a specific attribute of a button."""

    enabled: Tuple[str, str]
    disabled: Tuple[str, str]


class Style(TypedDict):
    """Defines the complete style configuration for a button."""

    fg_color: ColorState
    border_color: ColorState
    hover_color: Tuple[str, str]
    text_color: Tuple[str, str]
    text_color_disabled: Tuple[str, str]


class Button(ctk.CTkButton):
    """A customizable button with styles, localization, and enable/disable states."""

    def __init__(
            self,
            parent,
            label_key: str,
            style: str = 'default',
            command: Optional[Callable[[str], None]] = None,
            is_disabled: bool = False,
            **kwargs
    ):
        """
        Initialise Button widget.

        :param parent: The parent widget were button should be placed.
        :param loc_label_key: Localisation key for the button label.
        :param style: Variant of the button (primary, secondary, danger)
        :param command: Function to assign with button (when clicking)
        :param is_disabled: Whether the button starts disabled, by default False.
        :param kwargs: Additional keyword arguments.
        """
        self.localisation = localisation
        self.style = style
        self.is_disabled = is_disabled

        self.key = label_key

        super().__init__(
            parent,
            text='',
            height=buttons.BUTTON_HEIGHT,
            border_width=1,
            command=command,
            **kwargs
        )

        self.propagate(False)
        self.configure(width=buttons.BUTTON_WIDTH, height=buttons.BUTTON_HEIGHT)

        self.set_style()

        if self.is_disabled:
            self.disable()

        self.localisation.bind(
            self,
            label_key
        )

    def reset(self):
        """Reset the button."""
        self.localisation.bind(self, self.key)

    def set_command(self, function):
        """Set specified command for the button."""
        self.configure(command=function)

    def set_style(self):
        """Apply style based on the button's state (enabled/disabled) and style."""
        styles: Dict[str, Style] = {
            'default': {
                'fg_color': {
                    'enabled': buttons.BUTTON_DEFAULT_FG_COLOR,
                    'disabled': buttons.BUTTON_DEFAULT_FG_COLOR_DISABLED
                },
                'border_color': {
                    'enabled': buttons.BUTTON_DEFAULT_BORDER,
                    'disabled': buttons.BUTTON_DEFAULT_BORDER_DISABLED
                },
                'hover_color': buttons.BUTTON_DEFAULT_FG_COLOR_HOVER,
                'text_color': buttons.BUTTON_DEFAULT_TEXT,
                'text_color_disabled': buttons.BUTTON_DEFAULT_TEXT_DISABLED
            },
            'primary': {
                'fg_color': {
                    'enabled': buttons.BUTTON_PRIMARY_FG_COLOR,
                    'disabled': buttons.BUTTON_PRIMARY_FG_COLOR_DISABLED
                },
                'border_color': {
                    'enabled': buttons.BUTTON_PRIMARY_BORDER,
                    'disabled': buttons.BUTTON_PRIMARY_BORDER_DISABLED
                },
                'hover_color': buttons.BUTTON_PRIMARY_FG_COLOR_HOVER,
                'text_color': buttons.BUTTON_PRIMARY_TEXT,
                'text_color_disabled': buttons.BUTTON_PRIMARY_TEXT_DISABLED
            },
            'danger': {
                'fg_color': {
                    'enabled': buttons.BUTTON_DANGER_FG_COLOR,
                    'disabled': buttons.BUTTON_DANGER_FG_COLOR_DISABLED
                },
                'border_color': {
                    'enabled': buttons.BUTTON_DANGER_BORDER,
                    'disabled': buttons.BUTTON_DANGER_BORDER_DISABLED
                },
                'hover_color': buttons.BUTTON_DANGER_FG_COLOR_HOVER,
                'text_color': buttons.BUTTON_DANGER_TEXT,
                'text_color_disabled': buttons.BUTTON_DANGER_TEXT_DISABLED
            }
        }

        state: str = 'disabled' if self.is_disabled else 'enabled'
        style_config = styles.get(self.style)

        if style_config:
            fg_color = style_config['fg_color'].get(state)
            border_color = style_config['border_color'].get(state)

            hover_color = style_config['hover_color']
            text_color = style_config['text_color']
            text_color_disabled = style_config['text_color_disabled']
        else:
            fg_color = buttons.BUTTON_DEFAULT_FG_COLOR
            border_color = buttons.BUTTON_DEFAULT_BORDER

            hover_color = buttons.BUTTON_DEFAULT_FG_COLOR_HOVER
            text_color = buttons.BUTTON_DEFAULT_TEXT
            text_color_disabled = buttons.BUTTON_DEFAULT_TEXT_DISABLED

        self.configure(
            fg_color=fg_color,
            hover_color=hover_color,
            border_color=border_color,
            text_color=text_color,
            text_color_disabled=text_color_disabled
        )

    def get_state(self):
        """Return the state of the button."""
        return self.cget('state')

    def enable(self):
        """Enable the button, making it clickable."""
        self.is_disabled = False
        self.configure(state='normal')
        self.set_style()

    def disable(self):
        """Disable the button, preventing interaction."""
        self.configure(state='disabled')
        self.is_disabled = True
        self.set_style()
