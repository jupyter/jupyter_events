(defining-schema)=

# Defining an event schema

All Jupyter Events schemas are valid [JSON schema](https://json-schema.org/) and can be written in valid YAML or JSON. More specifically, these schemas are validated against Jupyter Event's "meta"-JSON schema, [here](https://github.com/jupyter/jupyter_events/tree/main/jupyter_events/schemas/event-metaschema.yml).

A common pattern is to define these schemas in separate files and register them with an `EventLogger` using the `.register_event_schema(...)` method:

```python
schema_filepath = "/path/to/schema.yaml"

logger = EventLogger()
logger.register_event_schema(schema_file)
```

At a minimum, a valid Jupyter event schema requires the following keys:

- `$id` : a URI to identify (and possibly locate) the schema.
- `version` : the schema version.
- `properties` : attributes of the event being emitted.

Beyond these required items, any valid JSON should be possible. Here is a simple example of a valid JSON schema for an event.

```yaml
$id: event.jupyter.org/example-event
version: 1
title: My Event
description: |
  Some information about my event
type: object
properties:
  thing:
    title: Thing
    description: A random thing.
  user:
    title: User name
    description: Name of user who initiated event
required:
  - thing
  - user
```
