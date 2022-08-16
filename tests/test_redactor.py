import io
import json
import logging

import pytest

from jupyter_events.logger import EventLogger
from jupyter_events.redactor import MaskRedactor, RemovalRedactor
from jupyter_events.schema import EventSchema

from .utils import SCHEMA_PATH


@pytest.fixture
def schema1():
    # Read schema from path.
    schema_path = SCHEMA_PATH / "good" / "user.yaml"
    return EventSchema(schema=schema_path)


@pytest.fixture
def schema2():
    # Read schema from path.
    schema_path = SCHEMA_PATH / "good" / "user2.yaml"
    return EventSchema(schema=schema_path)


@pytest.fixture
def sink():
    return io.StringIO()


@pytest.fixture
def handler(sink):
    return logging.StreamHandler(sink)


@pytest.fixture
def event_logger(handler, schema1, schema2):
    logger = EventLogger()
    logger.register_handler(handler)
    logger.register_event_schema(schema1)
    logger.register_event_schema(schema2)
    return logger


@pytest.fixture
def read_emitted_event(handler, sink):
    def _read():
        handler.flush()
        output = json.loads(sink.getvalue())
        # Clear the sink.
        sink.truncate(0)
        sink.seek(0)
        return output

    return _read


def test_mask_pattern_redactor(schema1, event_logger, read_emitted_event):
    redactor = MaskRedactor(redacted_patterns=["username"])

    # Add the modifier
    event_logger.add_modifier(redactor)
    data = {"name": "Alice", "username": "jovyan", "hobby": "Coding"}
    event_logger.emit(schema1.id, schema1.version, data)

    output = read_emitted_event()
    assert "username" in output
    assert output["username"] == "<masked>"

    # Check that everything else was unchanged
    assert "hobby" in output
    assert output["hobby"] == "Coding"
    assert "name" in output
    assert output["name"] == "Alice"


def test_mask_properties_redactor(schema1, schema2, event_logger, read_emitted_event):
    redactor = MaskRedactor(
        redacted_properties=[(schema1.id, schema1.version, "username")]
    )

    # Add the modifier
    event_logger.add_modifier(redactor)
    data = {"name": "Alice", "username": "jovyan", "hobby": "Coding"}
    event_logger.emit(schema1.id, schema1.version, data)

    output = read_emitted_event()
    assert "username" in output
    assert output["username"] == "<masked>"
    # Check that everything else was unchanged
    assert "hobby" in output
    assert output["hobby"] == "Coding"
    assert "name" in output
    assert output["name"] == "Alice"

    # Emit an event from the second schema to make sure
    # the properties were only applied to specific schema.
    data = {"name": "Alice", "username": "jovyan", "hobby": "Coding"}
    event_logger.emit(schema2.id, schema2.version, data)

    output = read_emitted_event()

    # Check that everything else was unchanged
    assert "username" in output
    assert output["username"] == "jovyan"
    assert "hobby" in output
    assert output["hobby"] == "Coding"
    assert "name" in output
    assert output["name"] == "Alice"


def test_mask_schemas_redactor(schema1, schema2, event_logger, read_emitted_event):
    redactor = MaskRedactor(redacted_schemas=[(schema1.id, 1)])

    # Add the modifier
    event_logger.add_modifier(redactor)
    data = {"name": "Alice", "username": "jovyan", "hobby": "Coding"}
    event_logger.emit(schema1.id, schema1.version, data)

    output = read_emitted_event()
    # Check that everything was changed
    assert "username" in output
    assert output["username"] == "<masked>"
    assert "hobby" in output
    assert output["hobby"] == "<masked>"
    assert "name" in output
    assert output["name"] == "<masked>"

    # Emit an event from the second schema to make sure
    # the properties were only applied to specific schema.
    data = {"name": "Alice", "username": "jovyan", "hobby": "Coding"}
    event_logger.emit(schema2.id, schema2.version, data)

    output = read_emitted_event()
    # Check that second event was unchanged
    assert "username" in output
    assert output["username"] == "jovyan"
    assert "hobby" in output
    assert output["hobby"] == "Coding"
    assert "name" in output
    assert output["name"] == "Alice"


def test_removal_redactor(schema1, event_logger, read_emitted_event):
    redactor = RemovalRedactor(redacted_patterns=["username"])

    # Add the modifier
    event_logger.add_modifier(redactor)

    data = {"name": "Alice", "username": "jovyan", "hobby": "Coding"}
    event_logger.emit(schema1.id, schema1.version, data)

    # Flush from the handler
    output = read_emitted_event()
    assert "username" not in output
    assert "hobby" in output
    assert "name" in output
