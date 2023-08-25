from unittest.mock import Mock, create_autospec

import pytest

from src.eventoolkit import Event, EventInputBridge, EventPublisher, EventsFactory


@pytest.fixture()
def events_factory() -> EventsFactory:
    return create_autospec(EventsFactory)


@pytest.fixture()
def publisher() -> EventPublisher:
    return create_autospec(EventPublisher)


@pytest.fixture()
def event() -> Event:
    return create_autospec(Event)


@pytest.fixture()
def sut(events_factory, publisher) -> EventInputBridge:
    return EventInputBridge(factory=events_factory, publisher=publisher)


class TestOnMessage:
    def test_publishes_event_created_by_factory(
        self, sut, event, events_factory, publisher
    ):
        events_factory.create = Mock(return_value=event)

        sut.on_message("foo")

        events_factory.create.assert_called_once_with(raw="foo")
        publisher.publish.assert_called_once_with(event)
