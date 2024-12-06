"""
Event handling class for managing subscribers and notifications.

This class provides a simple pub-sub model for GUI components and managers.
"""

from typing import Any, Callable, List


class Event:
    """Represents an event with subscribe and notify methods for listeners."""

    def __init__(self):
        """Initialize an Event with an empty list of listeners."""
        self.listeners: List[Callable[..., None]] = []

    def subscribe(self, listener: Callable[..., None]) -> None:
        """
        Add a listener function to be called when the event is triggered.

        :param listener: Callable function or method to subscribe to the event.
        """
        if listener not in self.listeners:
            self.listeners.append(listener)

    def unsubscribe(self, listener: Callable[..., None]) -> None:
        """
        Remove a listener function from the event.

        :param listener: Callable function or method to unsubscribe.
        """
        if listener in self.listeners:
            self.listeners.remove(listener)

    def notify(self, *args: Any, **kwargs: Any) -> None:
        """
        Call all subscribed listeners with provided arguments.

        :param args: Positional arguments to pass to listeners.
        :param kwargs: Keyword arguments to pass to listeners.
        """
        for listener in self.listeners:
            listener(*args, **kwargs)
