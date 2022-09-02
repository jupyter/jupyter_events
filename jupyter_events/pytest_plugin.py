import io
import json
import logging

import pytest

from jupyter_events import EventLogger


@pytest.fixture
def jp_event_sink():
    """A stream for capture events."""
    return io.StringIO()


@pytest.fixture
def jp_event_handler(jp_event_sink):
    """A logging handler that captures any events emitted by the event handler"""
    return logging.StreamHandler(jp_event_sink)


@pytest.fixture
def jp_read_emitted_event(jp_event_handler, jp_event_sink):
    """Reads the last event emitted by the event_logger fixture"""

    def _read():
        jp_event_handler.flush()
        output = json.loads(jp_event_sink.getvalue())
        # Clear the sink.
        jp_event_sink.truncate(0)
        jp_event_sink.seek(0)
        return output

    return _read


@pytest.fixture
def jp_event_schemas():
    """A list of schema references.

    Each item should be one of the following:
    - string of serialized JSON/YAML content representing a schema
    - a pathlib.Path object pointing to a schema file on disk
    - a dictionary with the schema data.
    """
    return []


@pytest.fixture
def jp_event_logger(jp_event_handler, jp_event_schemas):
    """A pre-configured event logger for tests."""
    logger = EventLogger()
    for schema in jp_event_schemas:
        logger.register_event_schema(schema)
    logger.register_handler(handler=jp_event_handler)
    return logger
