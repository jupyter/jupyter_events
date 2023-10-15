(first-event)=

# Logging your first event!

The `EventLogger` is the main object in Jupyter Events.

```python
from jupyter_events.logger import EventLogger

logger = EventLogger()
```

To begin emitting events from a Python application, you need to tell the `EventLogger` what events you'd like to emit. To do this, we should register our event's schema (more on this later) with the logger.

```python
schema = """
$id: http://myapplication.org/example-event
version: 1
title: Example Event
description: An interesting event to collect
properties:
   name:
      title: Name of Event
      type: string
"""


logger.register_event_schema(schema)
```

Now that the logger knows about the event, it needs to know _where_ to send it. To do this, we register a logging _Handler_ —borrowed from Python's standard [`logging`](https://docs.python.org/3/library/logging.html) library—to route the events to the proper place.

```python
# We will import one of the handlers from Python's logging library
from logging import StreamHandler

handler = StreamHandler()

logger.register_handler(handler)
```

The logger knows about the event and where to send it; all that's left is to emit an instance of the event! To to do this, call the `.emit(...)` method and set the (required) `schema_id` and `data` arguments.

```python
from jupyter_events import Event

logger.emit(
    schema_id="http://myapplication.org/example-event", data={"name": "My Event"}
)
```

On emission, the following data will get printed to your console by the `StreamHandler` instance:

```
{'__timestamp__': '2022-08-09T17:15:27.458048Z',
 '__schema__': 'myapplication.org/example-event',
 '__schema_version__': 1,
 '__metadata_version__': 1,
 'name': 'My Event'}
```
