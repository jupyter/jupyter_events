# Jupyter Events

*An event system for Jupyter Applications and extensions.*

Jupyter Events enables Jupyter Applications (e.g. Jupyter Server, Jupyter Notebook, JupyterLab, JupyterHub, etc.) to emit **events**—i.e. actions by application users—to remote (or local) destinations as **structured** data. It works with Python's standard `logging` library to handle the transmission of events allowing users to send events to local files, over the web, etc.

## Install

The Jupyter Events library can be installed from PyPI.
```
pip install jupyter_events
```

## Basic Usage

Jupyter Events provides a configurable traitlets object, `EventLogger`, for emitting structured event data in Python. It leverages Python's standard `logging` library for filtering, routing, and emitting events. All events are validated (using [jsonschema](https://pypi.org/project/jsonschema/)) against registered [JSON schemas](https://json-schema.org/).

Let's look at a basic example of an `EventLogger`.
```python
import logging
from jupyter_events import EventLogger


logger = EventLogger(
    # Use logging handlers to route where events
    # should be record.
    handlers=[
        logging.FileHandler('events.log')
    ],
    # List schemas of events that should be recorded.
    allowed_schemas=[
        'uri.to.event.schema'
    ]
)
```

EventLogger has two configurable traits:
* `handlers`: a list of Python's `logging` handlers.
* `allowed_schemas`: a list of event schemas to record.

Event schemas must be registered with the `EventLogger` for events to be recorded. An event schema looks something like:
```json
{
  "$id": "url.to.event.schema",
  "title": "My Event",
  "description": "All events must have a name property.",
  "type": "object",
  "properties": {
    "name": {
      "title": "Name",
      "description": "Name of event",
      "type": "string"
    }
  },
  "required": ["name"],
  "version": 1
}
```
2 fields are required:
* `$id`: a valid URI to identify the schema (and possibly fetch it from a remote address).
* `version`: the version of the schema.

The other fields follow standard JSON schema structure.

Schemas can be registered from a Python `dict` object, a file, or a URL. This example loads the above example schema from file.
```python
# Register the schema.
logger.register_schema_file('schema.json')
```

Events are recorded using the `record_event` method. This method validates the event data and routes the JSON string to the Python `logging` handlers listed in the `EventLogger`.
```python
# Record an example event.
event = {'name': 'example event'}
logger.record_event(
    schema_id='url.to.event.schema',
    version=1,
    event=event
)
```
