from collections.abc import Callable
from unittest.mock import PropertyMock, create_autospec

import pytest

from src.eventoolkit import Event, EventHandler, EventPublisher
from tests.helpers import not_raises


class FooEvent(Event):
    @property
    def name(self) -> str:
        return "foo"


class BarEvent(Event):
    @property
    def name(self) -> str:
        return "bar"


@pytest.fixture()
def create_handler() -> Callable[[type[Event]], EventHandler]:
    def factory(event_type: type[Event]) -> EventHandler:
        handler = create_autospec(EventHandler)
        type(handler).event_type = PropertyMock(return_value=event_type)
        return handler

    return factory


@pytest.fixture()
def event_foo() -> FooEvent:
    return FooEvent()


@pytest.fixture()
def event_bar() -> BarEvent:
    return BarEvent()


@pytest.fixture()
def sut() -> EventPublisher:
    return EventPublisher()


class TestSubscribe:
    def test_when_event_published_after_subscribing__handle_is_called(
        self, sut, event_foo, create_handler
    ):
        handler = create_handler(FooEvent)

        sut.subscribe(handler)
        sut.publish(event_foo)

        handler.handle.assert_called_once_with(event_foo)

    def test_when_subscribing_twice__publishing_events_call_handle_once(
        self, sut, event_foo, create_handler
    ):
        handler = create_handler(FooEvent)

        sut.subscribe(handler)
        sut.subscribe(handler)
        sut.publish(event_foo)

        handler.handle.assert_called_once_with(event_foo)

    def test_when_subscribed_to_event_foo__publishing_event_bar_does_not_call_handle(
        self, sut, event_bar, create_handler
    ):
        handler = create_handler(FooEvent)

        sut.subscribe(handler)
        sut.publish(event_bar)

        handler.handle.assert_not_called()


class TestUnsubscribe:
    def test_when_unsubscribing_not_previously_subscribed__does_not_raise(
        self, sut, create_handler
    ):
        handler = create_handler(FooEvent)

        with not_raises(Exception):
            sut.unsubscribe(handler)

    def test_when_event_published_after_unsubscribing__does_not_call_handle(
        self, sut, event_foo, create_handler
    ):
        handler = create_handler(FooEvent)

        sut.subscribe(handler)
        sut.unsubscribe(handler)
        sut.publish(event_foo)

        handler.handle.assert_not_called()


class TestPublish:
    def test_calls_handle_on_handlers_for_event_type(
        self, sut, create_handler, event_foo
    ):
        handler_1 = create_handler(FooEvent)
        handler_2 = create_handler(FooEvent)
        handler_3 = create_handler(BarEvent)
        sut.subscribe(handler_1)
        sut.subscribe(handler_2)
        sut.subscribe(handler_3)

        sut.publish(event_foo)

        handler_1.handle.assert_called_once_with(event_foo)
        handler_2.handle.assert_called_once_with(event_foo)
        handler_3.handle.assert_not_called()
