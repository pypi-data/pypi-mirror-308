"""
AttemptsList frame for displaying attempted characters.

AttemptsList extends BaseScrollFrame to show a list of guessed characters,
updating dynamically as attempts are made.
"""

from letterguesser.gui.widgets.List import List
from letterguesser.styles.padding import pad_2, pad_3

from .BaseScrollFrame import BaseScrollFrame


class AttemptsList(BaseScrollFrame):
    """
    Frame to display a scrollable list of attempted characters.

    This frame shows each guessed character along with its attempt
    number, updating in real time as new attempts are made.
    """

    def __init__(self, parent, **kwargs):
        """
        Initialize AttemptsList with title and update list on creation.

        :param parent: Parent object for the list frame.
        """
        super().__init__(
            parent,
            title_key='guessed_chars',
            **kwargs
        )

        self.list = List(self)

        self.set_placeholder('table_placeholder')
        self.update_list()

    def update_list(self):
        """Update display to show guessed characters or placeholder if empty."""
        data = self.list.get_items()

        if not data:
            self.show_placeholder()
            self.list.pack_forget()
        else:
            self.hide_placeholder()
            self.list.pack(
                side='top',
                fill='both',
                expand=True,
                padx=pad_3,
                pady=(pad_2, pad_3)
            )

    def add_char(self, char, attempt):
        """
        Add a character to the list with binary position tracking.

        :param char: Character to add.
        :param attempt: Attempt number for positional tracking.
        """
        alphabet_len = len(self.localisation.get_alphabet())

        binary = ['0'] * alphabet_len
        if attempt <= alphabet_len:
            binary[attempt - 1] = '1'

        binary_string = ''.join(binary)
        res = {
            'leading': {'key': 'attempt', 'value': attempt},
            'trailing': {'key': 'char', 'value': char},
            'sub': {'key': None, 'value': binary_string}
        }

        self.list.add_item(res)
        self.update_list()

    def reset(self):
        """Clear all entries from the list."""
        self.list.clear()
        self.update_list()
