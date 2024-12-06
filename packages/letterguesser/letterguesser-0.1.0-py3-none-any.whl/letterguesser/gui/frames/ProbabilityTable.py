"""
ProbabilityTable for displaying probability values in a table.

This frame manages a table that shows probabilities related to attempts.
"""

import customtkinter as ctk

from .BaseTable import BaseTable


class ProbabilityTable(BaseTable):
    """
    Table to display attempt probabilities in a scrollable layout.

    This table provides headers for attempt number and probability.
    """

    def __init__(self, parent, rows: int, **kwargs):
        """
        Initialize ProbabilityTable with rows and default headers.

        :param parent: The parent tkinter object.
        :param rows: The number of rows in the table.
        :param kwargs: Additional keyword arguments for table configuration.
        """
        super().__init__(
            parent,
            title_key='probability',
            columns=2,
            rows=rows
        )
        self.headers = ["", ""]
        self.header_keys = ['attempt', 'probability']
        self.header_labels: dict[str, str] = {}

        self.set_placeholder('table_placeholder')
        self.bind_headers()

    def reset_table(self):
        """Reset the table."""
        self.reset()

    def bind_headers(self):
        """Binds headers to localisation keys."""
        for i, key in enumerate(self.header_keys):
            label = ctk.CTkLabel(self, text='')
            self.header_labels[key] = label
            self.localisation.bind(
                label,
                key,
                lambda text, index=i: self.update_header(text, index)
            )

    def update_header(self, text, index):
        """Update the header text at the specified index."""
        self.headers[index] = text
        self.update_table()

    def init(self):
        """Initialize the table."""
        self.data = [self.headers] + [
            [i, 0] for i in range(1, len(self.localisation.get_alphabet()) + 1)
        ]
        self.update_table()

    def update_prob(self, index, new_value: int | float):
        """
        Update the probability value in the table at a specified row index.

        :param index: Row index to update.
        :param new_value: The new probability value.
        """
        if 1 <= index <= len(self.data) - 1:
            self.data[index][1] = new_value
            self.update_table()
