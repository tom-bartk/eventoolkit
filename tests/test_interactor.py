from unittest.mock import call, create_autospec

import pytest

from src.eventoolkit import EventHandler, EventPublisher, EventsObserver


@pytest.fixture()
def handler_1() -> EventHandler:
    return create_autospec(EventHandler)


@pytest.fixture()
def handler_2() -> EventHandler:
    return create_autospec(EventHandler)


@pytest.fixture()
def publisher() -> EventPublisher:
    return create_autospec(EventPublisher)


@pytest.fixture()
def sut(handler_1, handler_2, publisher) -> EventsObserver:
    return EventsObserver(handler_1, handler_2, publisher=publisher)


class TestObserve:
    def test_subscribes_handlers_to_publisher(self, sut, handler_1, handler_2, publisher):
        expected_calls = [call(handler=handler_1), call(handler=handler_2)]

        sut.observe()

        publisher.subscribe.assert_has_calls(expected_calls)


class TestStop:
    def test_unsubscribes_handlers_from_publisher(
        self, sut, handler_1, handler_2, publisher
    ):
        expected_calls = [call(handler=handler_1), call(handler=handler_2)]

        sut.stop()

        publisher.unsubscribe.assert_has_calls(expected_calls)
