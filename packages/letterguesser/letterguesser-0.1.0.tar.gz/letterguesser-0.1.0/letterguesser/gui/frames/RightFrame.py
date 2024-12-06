"""
RightFrame displaying probability and attempts tables.

Contains frames for probability and attempt tracking in a vertical layout.
"""

from typing import Any

from letterguesser.styles.padding import pad_0, pad_2

from .AttemptsList import AttemptsList
from .BaseFrame import BaseFrame
from .ProbabilityTable import ProbabilityTable


class RightFrame(BaseFrame):
    """Frame with probability and attempts tables."""

    def __init__(self, parent, **kwargs):
        """
        Initialize RightFrame with probability and attempts tables.

        :param parent: The parent tkinter object.
        :param kwargs: Additional keyword arguments for frame configuration.
        """
        super().__init__(parent, transparent_bg=True, **kwargs)

        alphabet_len = len(self.localisation.get_alphabet())

        self.prob_table = ProbabilityTable(self, alphabet_len)
        self.add_widget(self.prob_table, side='top', pady=(pad_0, pad_2))

        self.attempts_table = AttemptsList(self)
        self.add_widget(self.attempts_table, side='bottom', pady=(pad_2, pad_0))

        self.manager.table_events['reset'].subscribe(self.table_reset)
        self.manager.table_events['update'].subscribe(self.table_update)
        self.manager.table_events['init'].subscribe(self.table_init)

    def table_update(
            self,
            table_name: str,
            update_method: str,
            *args: Any,
            **kwargs: Any
    ) -> None:
        """Update specified table using the given method and parameters."""
        if hasattr(self, table_name):
            table = getattr(self, table_name)

            method = getattr(table, update_method, None)
            if callable(method):
                method = getattr(table, update_method)
                method(*args, **kwargs)

    def table_reset(self, table_name: str) -> None:
        """Reset the specified table by name if it has reset() method."""
        if hasattr(self, table_name):
            table = getattr(self, table_name)

            if hasattr(table, 'reset'):
                table.reset()

    def table_init(self, table_name: str) -> None:
        """Init the specified table by name if it has an init() method."""
        if hasattr(self, table_name):
            table = getattr(self, table_name)

            if hasattr(table, 'init'):
                table.init()
