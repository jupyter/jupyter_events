# Adding event listeners

Event listeners are callback functions/methods that are executed when an event is emitted.

Listeners can be used by extension authors to trigger custom logic every time an event occurs.

## Basic usage

Define a listener function:

```python
from jupyter_events.logger import EventListenerData


def my_listener(event_data: EventListenerData) -> None:
    print("hello, from my listener")
```

Hook this listener to a specific event type:

```python
event_logger.add_listener("http://event.jupyter.org/my-event", version=1, listener=my_listener)
```

Now, every time a `"http://event.jupyter.org/test"` event is emitted from the EventLogger, this listener will be called.
