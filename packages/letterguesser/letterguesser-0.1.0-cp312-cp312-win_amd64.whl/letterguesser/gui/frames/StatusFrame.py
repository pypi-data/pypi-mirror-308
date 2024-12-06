"""
StatusFrame for displaying application status information.

This frame shows the current status or message to the user.
"""

from letterguesser.gui.widgets import TextBlockSegment
from letterguesser.styles.padding import pad_5

from .BaseFrame import BaseFrame


class StatusFrame(BaseFrame):
    """
    Frame for displaying status updates.

    Shows current application status using a text block.
    """

    def __init__(
            self,
            parent,
            **kwargs
    ):
        """
        Initialize StatusFrame with a status display.

        :param parent: The parent tkinter object.
        :param kwargs: Additional keyword arguments for frame configuration.
        """
        super().__init__(parent, **kwargs)

        self.status = TextBlockSegment(
            parent=self,
            localisation_key='status_label',
            initial_text='random_text'
        )

        self.add_widget(
            self.status,
            side='top',
            expand=False,
            fill='x',
            padx=pad_5, pady=pad_5
        )

        self.local_blocks = {
            'status': self.status
        }

        self.manager.block_events['rebind'].subscribe(self.status_rebind)
        self.manager.block_events['reset'].subscribe(self.status_reset)

    def status_rebind(self, block_name: str, key: str) -> None:
        """
        Rebind the status block to a new localisation key.

        :param block_name: Name of the block to rebind.
        :param key: New localisation key.
        """
        block = self.local_blocks.get(block_name)

        if block:
            self.status.rebind(key)

    def status_reset(self, block_name: str) -> None:
        """
        Reset the specified status block.

        :param block_name: Name of the block to reset.
        """
        block = self.local_blocks.get(block_name)

        if block:
            block.reset()
