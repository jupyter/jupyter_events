# Adding event listeners

Event listeners are asynchronous callback functions/methods that are triggered when an event is emitted.

Listeners can be used by extension authors to trigger custom logic every time an event occurs.

## Basic usage

Define a listener (async) function:

```python
from jupyter_events.logger import EventLogger


async def my_listener(logger: EventLogger, schema_id: str, data: dict) -> None:
    print("hello, from my listener")
```

Hook this listener to a specific event type:

```python
event_logger.add_listener(
    schema_id="http://event.jupyter.org/my-event", listener=my_listener
)
```

Now, every time a `"http://event.jupyter.org/test"` event is emitted from the EventLogger, this listener will be called.
