from abc import ABC, abstractmethod

from .event import Event

__all__ = ["EventsFactory"]


class EventsFactory(ABC):
    """Factory for creating events from text input."""

    __slots__ = ()

    @abstractmethod
    def create(self, raw: str) -> Event:
        """Create a new event from text.

        Args:
            raw (str): The input string.

        Returns:
            The created event.
        """
