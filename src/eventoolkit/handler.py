from collections.abc import Sequence
from typing import Generic, TypeVar

import pydepot

from .abc import Event, EventHandler

__all__ = ["StoreEventHandler"]

TEvent = TypeVar("TEvent", bound=Event)
"""Invariant type variable bound by an `Event`."""

TState = TypeVar("TState")
"""Invariant type variable for a generic state."""


class StoreEventHandler(Generic[TEvent, TState], EventHandler[TEvent]):
    """An event handler using a template method for processing events.

    Subclasses should override the `actions` method to return a list of
    actions based on the incoming `event`. Those actions are then going to be
    dispatched to the store.

    Use the `side_effect(event)` method to perform additional side effects after the
    actions have been dispatched.
    """

    __slots__ = ("_store",)

    def __init__(self, store: pydepot.Store[TState]):
        """Initialize new handler with store.

        Args:
            store (pydepot.Store[TState]): Store to dispatch actions to.
        """
        self._store: pydepot.Store[TState] = store

    def actions(self, event: TEvent) -> Sequence[pydepot.Action]:
        """Actions to dispatch to the store created from the event.

        Defaults to empty list.

        Args:
            event (TEvent): The incoming event.

        Returns:
            The actions to dispatch.
        """
        return []

    def side_effects(self, event: TEvent) -> None:
        """Perform side effects after receiving the event.

        Defaults to doing nothing.

        Args:
            event (TEvent): The incoming event.
        """

    def handle(self, event: TEvent) -> None:
        """The template method handling the event.

        First, the `actions` are dispatched to the store.
        Then, the `side_effects` are performed.
        """
        for action in self.actions(event):
            self._store.dispatch(action)
        self.side_effects(event)
