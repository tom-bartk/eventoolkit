from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .event import Event

__all__ = ["EventHandler"]

TEvent = TypeVar("TEvent", bound=Event)
"""Invariant type variable bound by an `Event`."""


class EventHandler(Generic[TEvent], ABC):
    """A base class for an event handler."""

    __slots__ = ()

    @property
    @abstractmethod
    def event_type(self) -> type[TEvent]:
        """The type of the `Event` that this handler handles."""

    @abstractmethod
    def handle(self, event: TEvent) -> None:
        """Handle an event.

        Args:
            event (TEvent): The event to handle.
        """
