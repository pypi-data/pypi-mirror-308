"""
BaseTable provides a scrollable table layout with placeholder support.

Extends BaseScrollFrame to support tabular data, with methods to set,
update, and reset table content. For table base uses CTkTable package.
"""

from CTkTable import CTkTable

from letterguesser.styles.padding import pad_2, pad_3

from .BaseScrollFrame import BaseScrollFrame


class BaseTable(BaseScrollFrame):
    """
    Scrollable frame for displaying table data with customizable columns.

    Designed for displaying tabular data in a scrollable format, with
    support for placeholders when no data is available.
    """

    def __init__(
            self,
            parent,
            title_key,
            columns,
            rows,
            **kwargs
    ):
        """
        Initialize BaseTable with title, column, and row setup.

        :param parent: Parent object for the table.
        :param title_key: Localisation key for the title.
        :param columns: Number of table columns.
        :param rows: Number of table rows.
        """
        super().__init__(parent, title_key=title_key, **kwargs)

        self.data = []

        self.table = CTkTable(self, row=rows, column=columns, corner_radius=8)
        self.table.pack_forget()

    def update_table(self):
        """Update table with data or show placeholder if no data."""
        if not self.data:
            self.show_placeholder()
            self.table.pack_forget()
        else:
            self.hide_placeholder()
            self.table.update_values(self.data)
            self.table.pack(fill='x', expand=True, padx=pad_3, pady=(pad_2, pad_3))

    def reset(self):
        """Clear table content and update display."""
        self.data = []
        self.update_table()

    def set_data(self, new_data):
        """
        Set new data for the table and refresh the view.

        :param new_data: List of data entries for the table.
        """
        self.data = new_data
        self.update_table()
