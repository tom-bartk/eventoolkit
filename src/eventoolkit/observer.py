from collections.abc import Sequence

from .abc import EventHandler
from .publisher import EventPublisher

__all__ = ["EventsObserver"]


class EventsObserver:
    """Observer that manages subscriptions of its event handlers."""

    __slots__ = ("_handlers", "_publisher")

    def __init__(self, *handlers: EventHandler, publisher: EventPublisher):
        """Initialize new instance with a publisher and event handlers.

        Args:
            *handlers (EventHandler): Event handlers to manage.
            publisher (EventPublisher): The publisher to subscribe handlers to.
        """
        self._handlers: Sequence[EventHandler] = handlers
        self._publisher: EventPublisher = publisher

    def observe(self) -> None:
        """Start observing for incoming events.

        Subscribes all handlers to the publisher.
        """
        for handler in self._handlers:
            self._publisher.subscribe(handler=handler)

    def stop(self) -> None:
        """Stop observing for incoming events.

        Unsubscribes all handlers from the publisher.
        """
        for handler in self._handlers:
            self._publisher.unsubscribe(handler=handler)
