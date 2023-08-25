from .abc import EventsFactory
from .publisher import EventPublisher

__all__ = ["EventInputBridge"]


class EventInputBridge:
    """Bridges text events producers and the publisher.

    Tip:
        The signature of `on_message(self, message: str) -> None` matches
        the `asockit.SocketReaderDelegate` from the `asockit` package.
        Eventoolkit works great with the `asockit.SocketReader` as the events producer.
    """

    __slots__ = ("_factory", "_publisher", "__weakref__")

    def __init__(self, factory: EventsFactory, publisher: EventPublisher):
        """Initialize new bridge with an events factory and the publisher.

        Args:
            factory (EventsFactory): The events factory.
            publisher (EventPublisher): The publisher.
        """
        self._factory: EventsFactory = factory
        self._publisher: EventPublisher = publisher

    def on_message(self, message: str) -> None:
        """Callback for incoming text events.

        Creates a new `Event` using the factory, and publishes it using the publisher.

        Args:
            message (str): The text representation of an event.
        """
        self._publisher.publish(self._factory.create(raw=message))
