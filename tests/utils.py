import io
import json
import logging
from copy import deepcopy

from jupyter_events.logger import EventLogger


def get_event_data(event, schema, schema_id, version, allowed_schemas):
    sink = io.StringIO()

    # Create a handler that captures+records events with allowed tags.
    handler = logging.StreamHandler(sink)

    e = EventLogger(handlers=[handler], allowed_schemas=allowed_schemas)
    e.register_schema(schema)

    # Record event and read output
    e.record_event(schema_id, version, deepcopy(event))

    recorded_event = json.loads(sink.getvalue())
    return {
        key: value for key, value in recorded_event.items() if not key.startswith("__")
    }
