from collections.abc import Sequence
from typing import Any
from unittest.mock import Mock, call, create_autospec

import pytest
from pydepot import Action, Store

from src.eventoolkit import Event, StoreEventHandler
from tests.helpers import not_raises


class MockEvent(Event):
    @property
    def name(self) -> str:
        return "foo"


class DefaultStoreEventHandler(StoreEventHandler[MockEvent, Mock]):
    @property
    def event_type(self) -> type[MockEvent]:
        return MockEvent


class MockStoreEventHandler(StoreEventHandler[MockEvent, Mock]):
    @property
    def event_type(self) -> type[MockEvent]:
        return MockEvent

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.mock_actions: Mock = Mock(return_value=[])
        self.mock_side_effects: Mock = Mock()
        super().__init__(*args, **kwargs)

    def actions(self, event: MockEvent) -> Sequence[Action]:
        return self.mock_actions(event)

    def side_effects(self, event: MockEvent) -> None:
        self.mock_side_effects(event)


@pytest.fixture()
def store() -> Store:
    return create_autospec(Store)


@pytest.fixture()
def default_sut(store) -> StoreEventHandler:
    return DefaultStoreEventHandler(store=store)


@pytest.fixture()
def mock_sut(store) -> MockStoreEventHandler:
    return MockStoreEventHandler(store=store)


@pytest.fixture()
def event() -> MockEvent:
    return MockEvent()


class TestDefaults:
    def test_actions__returns_empty_list(self, default_sut, event):
        assert default_sut.actions(event=event) == []

    def test_side_effects__does_not_raise(self, default_sut, event):
        with not_raises(Exception):
            default_sut.side_effects(event=event)


class TestHandle:
    def test_dispatches_actions_to_store(self, mock_sut, event, store):
        action_1 = Mock()
        action_2 = Mock()
        mock_sut.mock_actions.return_value = [action_1, action_2]
        expected_calls = [call(action_1), call(action_2)]

        mock_sut.handle(event)

        store.dispatch.assert_has_calls(expected_calls)
        mock_sut.mock_actions.assert_called_once_with(event)

    def test_perfroms_side_effects(self, mock_sut, event):
        mock_sut.handle(event)

        mock_sut.mock_side_effects.assert_called_once_with(event)
