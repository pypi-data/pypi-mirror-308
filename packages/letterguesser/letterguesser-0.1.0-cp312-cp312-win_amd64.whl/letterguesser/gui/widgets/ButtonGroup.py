"""
ButtonGroup widget to manage a collection of buttons and option menus.

This class allows organizing multiple buttons with shared settings and access.
"""

from typing import Any, Dict, Union

from letterguesser.gui.frames.BaseFrame import BaseFrame
from letterguesser.styles.padding import pad_0, pad_2

from .Button import Button
from .OptionMenu import OptionMenu


def to_bool(value: str | bool) -> bool:
    """Convert string to bool."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("yes", "true", "t", "1")


def to_list(value: str | list[str]) -> list[str]:
    """Ensure the value is a list."""
    if isinstance(value, list):
        return [str(item) for item in value]
    elif isinstance(value, str):
        return [value]


class ButtonGroup(BaseFrame):
    """A container for managing buttons and option menus."""

    def __init__(
            self,
            parent: BaseFrame,
            configs: list[dict[str, Any]],
            gap: int = pad_2,
            **kwargs
    ):
        """
        Init ButtonGroup class.

        :param parent: The parent widget.
        :param configs: List of button configurations (label_key, style, etc.).
        :param gap: The gap between buttons, by default pad_2.
        :param kwargs: Additional keywords for CTkButton class
        """
        super().__init__(parent, transparent_bg=True, **kwargs)

        self.buttons: Dict[str, Union[Button, OptionMenu]] = {}

        for i, config in enumerate(configs):

            widget_type = config.get('type', 'button')

            if widget_type == 'button':
                is_disabled_ = config.get('is_disabled', False)
                is_disabled = to_bool(is_disabled_)

                command = config.get('command', None)

                item = Button(
                    parent=self,
                    label_key=config['label_key'],
                    style=config.get('style', 'default'),
                    command=command,
                    is_disabled=is_disabled
                )
            elif widget_type == 'option_menu':
                values_ = config.get('values', [])
                values = to_list(values_)

                command = config.get('command', None)

                item = OptionMenu(
                    parent=self,
                    label_key=config['label_key'],
                    initial_value=config.get('initial_value', ''),
                    values=values,
                    command=command
                )
            else:
                raise ValueError(f"Unsupported widget type: {widget_type}")

            self.add_widget(
                item,
                side='left',
                expand=False,
                fill='x',
                padx=(pad_0, gap) if i < len(configs) - 1 else pad_0,
            )

            self.buttons[f'button_{config["label_key"]}'] = item

    def get_button(self, key: str) -> Button | None:
        """
        Return a specific button by its `key` if available.

        :param key: The key of the button (e.g., 'button_<label_key>')
        :return: The Button instance or None if not found.
        """
        return self.buttons.get(key, None)

    def disable(self, key: str) -> None:
        """
        Disable the button identified by `key`.

        :param key: The identifier of the button to disable.
        :return: None
        """
        button = self.get_button(key)
        if button:
            button.disable()

    def enable(self, key: str) -> None:
        """
        Enable the button identified by `key`.

        :param key: The identifier of the button to enable.
        :return: None
        """
        button = self.get_button(key)
        if button:
            button.enable()

    def update_label(self, key: str, new_label_key: str) -> None:
        """
        Update the label of a button based on localisation key.

        :param key: Identifier for the target button.
        :param new_label_key: Localisation key for the new label text.
        :return: None
        """
        button = self.get_button(key)
        if button:
            button.localisation.bind(button, new_label_key)

    def enable_all(self) -> None:
        """Enable all buttons in the group."""
        for button in self.buttons.values():
            button.enable()

    def disable_all(self) -> None:
        """Disable all buttons in the group."""
        for button in self.buttons.values():
            button.disable()
