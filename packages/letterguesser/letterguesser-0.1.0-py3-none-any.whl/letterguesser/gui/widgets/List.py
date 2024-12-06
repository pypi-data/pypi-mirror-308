"""
List frame for displaying a collection of list items.

This frame manages a list of `ListItem` instances, each displaying structured data.
"""

from typing import Any

from letterguesser.gui.frames.BaseFrame import BaseFrame

from .ListItem import ListItem


class List(BaseFrame):
    """A scrollable list frame for adding, updating, and clearing items."""

    def __init__(self, parent, **kwargs):
        """Initialize the scrollable list frame."""
        super().__init__(parent, **kwargs)

        self.items = []

    def get_items(self) -> list[ListItem]:
        """
        Return all items in the list.

        :return: List of all `ListItem` objects.
        """
        return self.items if self.items else []

    def add_item(self, data: dict[str, Any]) -> None:
        """
        Add a new item to the list.

        :param data: Data to be displayed in the new list item.
        """
        is_odd = len(self.items) % 2 == 1
        item = ListItem(self, data, is_odd)
        self.add_widget(item, fill='x')

        self.items.append(item)

    def clear(self):
        """Remove all items from the list."""
        for item in self.items:
            item.destroy()
        self.items.clear()
