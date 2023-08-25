from typing import TypeVar
from weakref import WeakSet

from .abc import Event, EventHandler

__all__ = ["EventPublisher"]

TEvent = TypeVar("TEvent", bound=Event, covariant=True)
"""Covariant type variable bound by an `Event`."""


class EventPublisher:
    """A central publisher of incoming events.

    Serves as an event bus, which accepts events from external producers,
    and passes them to currenty subscribed handlers with a matching event type.
    """

    __slots__ = ("_handlers", "__weakref__")

    def __init__(self) -> None:
        """Initialize new publisher."""
        self._handlers: dict[type[Event], WeakSet[EventHandler]] = {}

    def subscribe(self, handler: EventHandler[TEvent]) -> None:
        """Subscribe an event handler.

        When an event with a matching type is published, the `handler.handle`
        will be called with the incoming event.

        This method is idempotent - multiple calls will not cause multiple subscriptions.

        Make sure to keep a strong reference to the handler, because the publisher only
        keeps a weak reference.

        Args:
            handler (EventHandler[TEvent]): The handler to subscribe.
        """
        if subscribers := self._handlers.get(handler.event_type, None):
            subscribers.add(handler)
        else:
            self._handlers[handler.event_type] = WeakSet([handler])

    def unsubscribe(self, handler: EventHandler[TEvent]) -> None:
        """Unsubscribe an event handler.

        The `handler` will no longer receive new events.

        Args:
            handler (EventHandler[TEvent]): The handler to unsubscribe.
        """
        if current_subscribers := self._handlers.get(handler.event_type, None):
            current_subscribers.discard(handler)

    def publish(self, event: Event) -> None:
        """Publish an event.

        Every currently subscribed handler, that has the `event_type` equal to that of
        the `event`, will be notified using the `handle` method.

        Args:
            event (Event): The event to publish.
        """
        if subscribers := self._handlers.get(type(event), None):
            for handler in subscribers.copy():
                handler.handle(event)
