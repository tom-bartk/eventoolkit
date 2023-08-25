## Manage multiple handlers with EventsObserver

A common pattern is to manage subscriptions of several event handlers at once.
The [`EventsObserver`](/api/observer/#eventoolkit.EventsObserver) is designed to solve this problem by providing a simple interface to subscribe / unsubscribe many handlers at once:

```python3
import eventoolkit

def main() -> None:
    handler_one = EventOneHandler()
    handler_two = EventTwoHandler()

    publisher = eventoolkit.EventPublisher()

    observer = eventoolkit.EventsObserver(
        handler_one, handler_two, publisher=publisher
    )

    # The handlers are now subscribed and ready to handle events.
    observer.observe()

    ...

    # The handlers are now unsubscribed from the publisher.
    observer.stop()
```

## Create events from text using EventsFactory 

Events often arrive as serialized strings. Use the [`EventsFactory`](/api/factory/#eventoolkit.abc.EventsFactory) to create event objects from, for example, JSON documents:

```python3
import json

import eventoolkit


class JsonEventsFactory(eventoolkit.EventsFactory):
    def create(self, raw: str) -> eventoolkit.Event:
        event = json.loads(raw)
        match event["name"]:
            case "event_one":
                return EventOne()
            case "event_two":
                return EventTwo()
            case _:
                raise NotImplementedError

```
## Publish events from TCP sockets

Eventoolkit works great when combined with [`asockit`](https://asockit.tombartk.com) - a toolkit for sockets.

The [`EventInputBridge`](/api/bridge/#eventoolkit.EventInputBridge) is a valid [`asockit.SocketReaderDelegate`](https://asockit.tombartk.com/api/reader/#asockit.SocketReaderDelegate), which makes publishing events read from TCP sockets very easy:

```python3
import asockit
import eventoolkit

...

async def main() -> None:
    publisher = EventPublisher()
    bridge = EventInputBridge(factory=JsonEventsFactory(), publisher=publisher)

    stream_reader, _ = await asyncio.open_connection("localhost", port=3000)
    reader = asockit.SocketReader(asockit.AsyncioReadableConnection(stream_reader))
    reader.set_delegate(bridge)

    await reader.start()
```



Whenever the [`asockit.SocketReader`](https://asockit.tombartk.com/api/reader/#asockit.SocketReader) reads a line from the socket, it will automatically be converted to an event, and published using the publisher.

