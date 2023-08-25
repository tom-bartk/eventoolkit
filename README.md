<div align="center">
  <a href="https://github.com/tom-bartk/eventoolkit">
    <img src="https://eventoolkit.tombartk.com/images/logo.png" alt="Logo" width="381" height="75">
  </a>

<div align="center">
<a href="https://jenkins.tombartk.com/job/eventoolkit/">
  <img alt="Jenkins" src="https://img.shields.io/jenkins/build?jobUrl=https%3A%2F%2Fjenkins.tombartk.com%2Fjob%2Feventoolkit">
</a>
<a href="https://jenkins.tombartk.com/job/eventoolkit/lastCompletedBuild/testReport/">
  <img alt="Jenkins tests" src="https://img.shields.io/jenkins/tests?jobUrl=https%3A%2F%2Fjenkins.tombartk.com%2Fjob%2Feventoolkit">
</a>
<a href="https://jenkins.tombartk.com/job/eventoolkit/lastCompletedBuild/coverage/">
  <img alt="Jenkins Coverage" src="https://img.shields.io/jenkins/coverage/apiv4?jobUrl=https%3A%2F%2Fjenkins.tombartk.com%2Fjob%2Feventoolkit%2F">
</a>
<a href="https://www.gnu.org/licenses/agpl-3.0.en.html">
  <img alt="PyPI - License" src="https://img.shields.io/pypi/l/eventoolkit">
</a>
<a href="https://pypi.org/project/eventoolkit/">
  <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/eventoolkit">
</a>
<a href="https://pypi.org/project/eventoolkit/">
  <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/eventoolkit">
</a>
<a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff" style="max-width:100%;"></a>
</div>

  <p align="center">
    Client-side toolkit for abstract events.
    <br />
    <a href="https://eventoolkit.tombartk.com"><strong>Documentation</strong></a>
  </p>
</div>

## Simple example

```python3
# main.py

from collections.abc import Sequence
from typing import NamedTuple

import pydepot

from eventoolkit import Event, EventPublisher, StoreEventHandler


class Chatroom(NamedTuple):
    users: tuple[str, ...]


class State(NamedTuple):
    chatroom: Chatroom


class StateSubscriber:
    def on_state(self, state: State) -> None:
        print(f"[StoreSubscriber] on_state called with {state}")


class JoinUserAction(pydepot.Action):
    def __init__(self, user: str):
        self.user: str = user


class JoinUserReducer(pydepot.Reducer[JoinUserAction, State]):
    @property
    def action_type(self) -> type[JoinUserAction]:
        return JoinUserAction

    def apply(self, action: JoinUserAction, state: State) -> State:
        return State(chatroom=Chatroom(users=(*state.chatroom.users, action.user)))


class UserJoinedEvent(Event):
    @property
    def name(self) -> str:
        return "user_joined"

    def __init__(self, user: str):
        self.user: str = user


class UserJoinedEventHandler(StoreEventHandler[UserJoinedEvent, State]):
    @property
    def event_type(self) -> type[UserJoinedEvent]:
        return UserJoinedEvent

    def actions(self, event: UserJoinedEvent) -> Sequence[pydepot.Action]:
        return [JoinUserAction(user=event.user)]


def main() -> None:
    store = pydepot.Store(State(chatroom=Chatroom(users=())))
    store.register(JoinUserReducer())

    subscriber = StateSubscriber()
    store.subscribe(subscriber)

    handler = UserJoinedEventHandler(store=store)

    publisher = EventPublisher()
    publisher.subscribe(handler)

    publisher.publish(UserJoinedEvent(user="Alice"))
    publisher.publish(UserJoinedEvent(user="Bob"))


if __name__ == "__main__":
    main()
```

```sh
$ python3 main.py

[StoreSubscriber] on_state called with
    State(chatroom=Chatroom(users=('Alice',)))

[StoreSubscriber] on_state called with
    State(chatroom=Chatroom(users=('Alice', 'Bob')))
```

## Installation

Eventoolkit is available as [`eventoolkit`](https://pypi.org/project/eventoolkit/) on PyPI:

```shell
pip install eventoolkit
```

## Usage

For detailed quickstart and API reference, visit the [Documentation](https://eventoolkit.tombartk.com/quickstart/).


## License
![AGPLv3](https://www.gnu.org/graphics/agplv3-with-text-162x68.png)
```monospace
Copyright (C) 2023 tombartk 

This program is free software: you can redistribute it and/or modify it under the terms
of the GNU Affero General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program.
If not, see https://www.gnu.org/licenses/.
```
