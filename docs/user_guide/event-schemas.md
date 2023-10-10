# What is an event schema?

A Jupyter event schema defines the _shape_ and _type_ of an emitted event instance. This is a key piece of Jupyter Events. It tells the event listeners what they should expect when an event occurs.

In the {ref}`first-event`, you saw how to register a schema with the `EventLogger`.

In the next section, {ref}`defining-schema`, you will learn how to define a new schema.

_So what exactly happens when we register a schema?_

```python
from jupyter_events.logger import EventLogger

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

logger = EventLogger()
logger.register_event_schema(schema)
```

First, the schema is validated against [Jupyter Event's metaschema](https://github.com/jupyter/jupyter_events/tree/main/jupyter_events/schemas/event-metaschema.yml). This ensures that your schema adheres minimally to Jupyter Event's expected form (read about how to define a schema [here](../user_guide/defining-schema.md)).

Second, a `jsonschema.Validator` is created and cached for each one of your event schemas in a "schema registry" object.

```python
print(logger.schemas)
```

```
Validator class: Draft7Validator
Schema: {
  "$id": "myapplication.org/example-event",
  "version": 1,
  "title": "Example Event",
  "description": "An interesting event to collect",
  "properties": {
    "name": {
      "title": "Name of Event",
      "type": "string"
    }
  }
}
```

The registry's validators will be used to check incoming events to ensure all outgoing, emitted events are registered and follow the expected form.

Lastly, if an incoming event is not found in the registry, it does not get emitted. This ensures that we only collect data that we explicitly register with the logger.
