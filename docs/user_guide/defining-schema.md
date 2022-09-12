(defining-schema)=

# Defining an event schema

All Jupyter Events schemas are valid [JSON schema](https://json-schema.org/) and can be written in valid YAML or JSON. More specifically, these schemas are validated against Jupyter Event's "meta"-JSON schema, [here](https://github.com/jupyter/jupyter_events/tree/main/jupyter_events/schemas/event-metaschema.yml).

A common pattern is to define these schemas in separate files and register them with an `EventLogger` using the `.register_event_schema(...)` method:

```python
schema_filepath = Path("/path/to/schema.yaml")

logger = EventLogger()
logger.register_event_schema(schema_file)
```

Note that a file path passed to `register_event_schema()` **must** be a Pathlib
object. This is required for `register_event_schema()` to distinguish between
file paths and schemas specified in a Python string.

At a minimum, a valid Jupyter event schema requires the following keys:

- `$id` : a URI to identify (and possibly locate) the schema.
- `version` : the schema version.
- `properties` : attributes of the event being emitted.

Beyond these required items, any valid JSON should be possible. Here is a simple example of a valid JSON schema for an event.

```yaml
$id: https://event.jupyter.org/example-event
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

## Checking if a schema is valid

When authoring a schema, how do you check if you schema is following the expected form? Jupyter Events offers a simple command line tool to validate your schema against its Jupyter Events metaschema.

First, install the CLI:

```
pip install "jupyter_events[cli]"
```

Then, run the CLI against your schema:

```
jupyter-events validate path/to/my_schema.json
```

The output will look like this, if it passes:

```
──────────────────────────────────── Validating the following schema ────────────────────────────────────

    {
      "$id": "http://event.jupyter.org/test",
      "version": 1,
      "title": "Simple Test Schema",
      "description": "A simple schema for testing\n",
      "type": "object",
      "properties": {
        "prop": {
          "title": "Test Property",
          "description": "Test property.",
          "type": "string"
        }
      }
    }

──────────────────────────────────────────────── Results ────────────────────────────────────────────────

✔ Nice work! This schema is valid.
```

or this if fails:

```
──────────────────────────────────── Validating the following schema ────────────────────────────────────

    {
      "$id": "http://event.jupyter.org/test",
      "version": 1,
      "title": "Simple Test Schema",
      "description": "A simple schema for testing\n",
      "type": "object",
      "properties": {
        "__badName": {
          "title": "Test Property",
          "description": "Test property.",
          "type": "string"
        }
      }
    }

──────────────────────────────────────────────── Results ────────────────────────────────────────────────
❌ The schema failed to validate.

We found the following error with your schema:

    '__badName' is an invalid property name because it starts with `__`. Properties starting with
    'dunder' are reserved as special meta-fields for Jupyter Events to use.
```
