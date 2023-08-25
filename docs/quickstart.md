## Define the State, an Action and a Reducer

Eventoolkit is designed to work with the Unidirectional Data Flow pattern implemented by the [`pydepot`](https://pydepot.tombartk.com) package. For detailed guide on how to set up `pydepot`, visit its [quickstart](https://pydepot.tombartk.com/quickstart/).

Following example defines a simple state and an action that joins a user to a chatroom:

```python3
from typing import NamedTuple

import pydepot


class Chatroom(NamedTuple):
    users: tuple[str, ...]


class State(NamedTuple):
    chatroom: Chatroom


class JoinUserAction(pydepot.Action):
    def __init__(self, user: str):
        self.user: str = user


class JoinUserReducer(pydepot.Reducer[JoinUserAction, State]):
    @property
    def action_type(self) -> type[JoinUserAction]:
        return JoinUserAction

    def apply(self, action: JoinUserAction, state: State) -> State:
        return State(chatroom=Chatroom(users=(*state.chatroom.users, action.user)))
```

## Define an Event

An [`Event`](/api/event/#eventoolkit.abc.Event) is an object describing something meaningful that happened inside a domain. In the chatroom example, the fact that a user joined the chatroom is a good example of an event:

```python3
import eventoolkit

...

class UserJoinedEvent(eventoolkit.Event):
    @property
    def name(self) -> str:
        return "user_joined"

    def __init__(self, user: str):
        self.user: str = user
```
## Create an EventHandler

To do something when an event is published, it needs an [`EventHandler`](/api/handler/#eventoolkit.abc.EventHandler). The [`StoreEventHandler`](/api/handler/#eventoolkit.StoreEventHandler) uses a [Template Method](https://refactoring.guru/design-patterns/template-method) to transform the event into a list of [pydepot.Action](https://pydepot.tombartk.com/api/action/#pydepot.abc.Action), which will then be dispatched to the [pydepot.Store](https://pydepot.tombartk.com/api/store/#pydepot.Store):

```python3
import eventoolkit

...

class UserJoinedEventHandler(eventoolkit.StoreEventHandler[UserJoinedEvent, State]):
    @property
    def event_type(self) -> type[UserJoinedEvent]:
        return UserJoinedEvent

    def actions(self, event: UserJoinedEvent) -> Sequence[pydepot.Action]:
        return [JoinUserAction(user=event.user)]
```

## Publish an Event

Before publishing an event, let's create a `StateSubscriber` that will print any changes to the `State` - this will help in verifying that the handler is doing its job:

```python3
...

class StateSubscriber:
    def on_state(self, state: State) -> None:
        print(f"[StoreSubscriber] on_state called with {state}")
```

Following example sets up the store, creates and subscribes the handler, and publishes two `UserJoinedEvent`: 

```python3
import eventoolkit

...

def main() -> None:
    store = pydepot.Store(State(chatroom=Chatroom(users=())))
    store.register(JoinUserReducer())

    subscriber = StateSubscriber()
    store.subscribe(subscriber)

    handler = UserJoinedEventHandler(store=store)

    publisher = eventoolkit.EventPublisher()
    publisher.subscribe(handler)

    publisher.publish(UserJoinedEvent(user="Alice"))
    publisher.publish(UserJoinedEvent(user="Bob"))


if __name__ == "__main__":
    main()
```

Running the script will result in the following output:

```sh
$ python3 main.py

[StoreSubscriber] on_state called with
    State(chatroom=Chatroom(users=('Alice',)))

[StoreSubscriber] on_state called with
    State(chatroom=Chatroom(users=('Alice', 'Bob')))
```

## Next steps

To see more in-depth examples, see the [Advanced Usage](/advanced/).

To see all available properties and methods, see the [API Documentation](/api/publisher/).
<br/>
