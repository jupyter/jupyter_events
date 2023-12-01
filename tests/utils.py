from __future__ import annotations

import io
import json
import logging
import pathlib
from copy import deepcopy

from jupyter_events.logger import EventLogger

SCHEMA_PATH = pathlib.Path(__file__).parent / "schemas"


def get_event_data(event, schema, schema_id, version, unredacted_policies):
    sink = io.StringIO()

    # Create a handler that captures+records events with allowed tags.
    handler = logging.StreamHandler(sink)

    e = EventLogger(handlers=[handler], unredacted_policies=unredacted_policies)
    e.register_event_schema(schema)

    # Record event and read output
    e.emit(schema_id=schema_id, data=deepcopy(event))

    recorded_event = json.loads(sink.getvalue())
    return {key: value for key, value in recorded_event.items() if not key.startswith("__")}
