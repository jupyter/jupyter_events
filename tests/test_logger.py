from __future__ import annotations

import io
import json
import logging
import sys
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import jsonschema
import pytest
from jsonschema.exceptions import ValidationError
from traitlets import TraitError
from traitlets.config.loader import PyFileConfigLoader

from jupyter_events import yaml
from jupyter_events.logger import EventLogger
from jupyter_events.schema_registry import SchemaRegistryException

GOOD_CONFIG = """
import logging

c.EventLogger.handlers = [
    logging.StreamHandler()
]
"""

BAD_CONFIG = """
import logging

c.EventLogger.handlers = [
    0
]
"""


def get_config_from_file(path, content):
    # Write config file
    filename = "config.py"
    config_file = path / filename
    config_file.write_text(content)

    # Load written file.
    loader = PyFileConfigLoader(filename, path=str(path))
    return loader.load_config()


def test_good_config_file(tmp_path):
    cfg = get_config_from_file(tmp_path, GOOD_CONFIG)

    # Pass config to EventLogger
    e = EventLogger(config=cfg)

    assert len(e.handlers) > 0
    assert isinstance(e.handlers[0], logging.Handler)


def test_bad_config_file(tmp_path):
    cfg = get_config_from_file(tmp_path, BAD_CONFIG)

    with pytest.raises(TraitError):
        EventLogger(config=cfg)


def test_register_invalid_schema():
    """
    Invalid JSON Schemas should fail registration
    """
    el = EventLogger()
    with pytest.raises(ValidationError):
        el.register_event_schema(
            {
                # Totally invalid
                "properties": True
            }
        )


def test_missing_required_properties():
    """
    id and $version are required properties in our schemas.

    They aren't required by JSON Schema itself
    """
    el = EventLogger()
    with pytest.raises(ValidationError):
        el.register_event_schema({"properties": {}})

    with pytest.raises(ValidationError):
        el.register_event_schema(
            {
                "$id": "something",
                "$version": 1,  # This should been 'version'
            }
        )


def test_timestamp_override():
    """
    Simple test for overriding timestamp
    """
    schema = {
        "$id": "http://test/test",
        "version": 1,
        "properties": {
            "something": {
                "type": "string",
                "title": "test",
            },
        },
    }

    output = io.StringIO()
    handler = logging.StreamHandler(output)
    el = EventLogger(handlers=[handler])
    el.register_event_schema(schema)

    timestamp_override = datetime.now(tz=timezone.utc) - timedelta(days=1)

    el.emit(
        schema_id="http://test/test",
        data={"something": "blah"},
        timestamp_override=timestamp_override,
    )
    handler.flush()
    event_capsule = json.loads(output.getvalue())
    assert event_capsule["__timestamp__"] == timestamp_override.isoformat() + "Z"


def test_emit():
    """
    Simple test for emitting valid events
    """
    schema = {
        "$id": "http://test/test",
        "version": 1,
        "properties": {
            "something": {
                "type": "string",
                "title": "test",
            }
        },
    }

    output = io.StringIO()
    handler = logging.StreamHandler(output)
    el = EventLogger(handlers=[handler])
    el.register_event_schema(schema)

    el.emit(
        schema_id="http://test/test",
        data={
            "something": "blah",
        },
    )
    handler.flush()

    event_capsule = json.loads(output.getvalue())

    assert "__timestamp__" in event_capsule
    # Remove timestamp from capsule when checking equality, since it is gonna vary
    del event_capsule["__timestamp__"]
    expected = {
        "__schema__": "http://test/test",
        "__schema_version__": 1,
        "__metadata_version__": 1,
        "something": "blah",
    }
    if sys.version_info >= (3, 12):
        expected["taskName"] = None
    assert event_capsule == expected


def test_message_field():
    """
    Simple test for emitting an event with
    the literal property "message".
    """
    schema = {
        "$id": "http://test/test",
        "version": 1,
        "properties": {
            "something": {
                "type": "string",
                "title": "test",
            },
            "message": {
                "type": "string",
                "title": "test",
            },
        },
    }

    output = io.StringIO()
    handler = logging.StreamHandler(output)
    el = EventLogger(handlers=[handler])
    el.register_event_schema(schema)

    el.emit(
        schema_id="http://test/test",
        data={"something": "blah", "message": "a message was seen"},
    )
    handler.flush()

    event_capsule = json.loads(output.getvalue())

    assert "__timestamp__" in event_capsule
    # Remove timestamp from capsule when checking equality, since it is gonna vary
    del event_capsule["__timestamp__"]
    expected = {
        "__schema__": "http://test/test",
        "__schema_version__": 1,
        "__metadata_version__": 1,
        "something": "blah",
        "message": "a message was seen",
    }
    if sys.version_info >= (3, 12):
        expected["taskName"] = None
    assert event_capsule == expected


def test_nested_message_field():
    """
    Simple test for emitting an event with
    the literal property "message".
    """
    schema = {
        "$id": "http://test/test",
        "version": 1,
        "properties": {
            "thing": {
                "type": "object",
                "title": "thing",
                "properties": {
                    "message": {
                        "type": "string",
                        "title": "message",
                    },
                },
            },
        },
    }

    output = io.StringIO()
    handler = logging.StreamHandler(output)
    el = EventLogger(handlers=[handler])
    el.register_event_schema(schema)

    el.emit(
        schema_id="http://test/test",
        data={"thing": {"message": "a nested message was seen"}},
    )
    handler.flush()

    event_capsule = json.loads(output.getvalue())

    assert "__timestamp__" in event_capsule
    # Remove timestamp from capsule when checking equality, since it is gonna vary
    del event_capsule["__timestamp__"]
    expected = {
        "__schema__": "http://test/test",
        "__schema_version__": 1,
        "__metadata_version__": 1,
        "thing": {"message": "a nested message was seen"},
    }
    if sys.version_info >= (3, 12):
        expected["taskName"] = None
    assert event_capsule == expected


def test_register_event_schema(tmp_path):
    """
    Register schema from a file
    """
    schema = {
        "$id": "http://test/test",
        "version": 1,
        "type": "object",
        "properties": {
            "something": {
                "type": "string",
                "title": "test",
            },
        },
    }

    el = EventLogger()
    schema_file = tmp_path.joinpath("schema.yml")
    yaml.dump(schema, schema_file)
    el.register_event_schema(schema_file)
    assert "http://test/test" in el.schemas


def test_register_event_schema_object(tmp_path):
    """
    Register schema from a file
    """
    schema = {
        "$id": "http://test/test",
        "version": 1,
        "type": "object",
        "properties": {
            "something": {
                "type": "string",
                "title": "test",
            },
        },
    }

    el = EventLogger()
    schema_file = tmp_path.joinpath("schema.yml")
    yaml.dump(schema, schema_file)
    el.register_event_schema(schema_file)

    assert "http://test/test" in el.schemas


def test_emit_badschema():
    """
    Fail fast when an event doesn't conform to its schema
    """
    schema = {
        "$id": "http://test/test",
        "version": 1,
        "type": "object",
        "properties": {
            "something": {
                "type": "string",
                "title": "test",
            },
            "status": {
                "enum": ["success", "failure"],
                "title": "test 2",
            },
        },
    }

    el = EventLogger(handlers=[logging.NullHandler()])
    el.register_event_schema(schema)

    with pytest.raises(jsonschema.ValidationError) as excinfo:
        el.emit(schema_id="http://test/test", data={"something": "blah", "status": "hi"})

    assert "'hi' is not one of" in str(excinfo.value)


def test_emit_badschema_format():
    """
    Fail fast when an event doesn't conform to a specific format
    """
    schema = {
        "$id": "http://test/test",
        "version": 1,
        "type": "object",
        "properties": {
            "something": {"type": "string", "title": "test", "format": "date-time"},
        },
    }

    el = EventLogger(handlers=[logging.NullHandler()])
    el.register_event_schema(schema)

    with pytest.raises(jsonschema.ValidationError) as excinfo:
        el.emit(schema_id="http://test/test", data={"something": "chucknorris"})

    assert "'chucknorris' is not a 'date-time'" in str(excinfo.value)


def test_unique_logger_instances():
    schema0 = {
        "$id": "http://test/test0",
        "version": 1,
        "type": "object",
        "properties": {
            "something": {
                "type": "string",
                "title": "test",
            },
        },
    }

    schema1 = {
        "$id": "http://test/test1",
        "version": 1,
        "type": "object",
        "properties": {
            "something": {
                "type": "string",
                "title": "test",
            },
        },
    }

    output0 = io.StringIO()
    output1 = io.StringIO()
    handler0 = logging.StreamHandler(output0)
    handler1 = logging.StreamHandler(output1)

    el0 = EventLogger(handlers=[handler0])
    el0.register_event_schema(schema0)

    el1 = EventLogger(handlers=[handler1])
    el1.register_event_schema(schema1)

    el0.emit(
        schema_id="http://test/test0",
        data={
            "something": "blah",
        },
    )
    el1.emit(
        schema_id="http://test/test1",
        data={
            "something": "blah",
        },
    )
    handler0.flush()
    handler1.flush()

    event_capsule0 = json.loads(output0.getvalue())

    assert "__timestamp__" in event_capsule0
    # Remove timestamp from capsule when checking equality, since it is gonna vary
    del event_capsule0["__timestamp__"]
    expected = {
        "__schema__": "http://test/test0",
        "__schema_version__": 1,
        "__metadata_version__": 1,
        "something": "blah",
    }
    if sys.version_info >= (3, 12):
        expected["taskName"] = None
    assert event_capsule0 == expected

    event_capsule1 = json.loads(output1.getvalue())

    assert "__timestamp__" in event_capsule1
    # Remove timestamp from capsule when checking equality, since it is gonna vary
    del event_capsule1["__timestamp__"]
    expected = {
        "__schema__": "http://test/test1",
        "__schema_version__": 1,
        "__metadata_version__": 1,
        "something": "blah",
    }
    if sys.version_info >= (3, 12):
        expected["taskName"] = None
    assert event_capsule1 == expected


def test_register_duplicate_schemas():
    schema0 = {
        "$id": "http://test/test",
        "version": 1,
        "type": "object",
        "properties": {
            "something": {
                "type": "string",
                "title": "test",
            },
        },
    }

    schema1 = {
        "$id": "http://test/test",
        "version": 1,
        "type": "object",
        "properties": {
            "something": {
                "type": "string",
                "title": "test",
            },
        },
    }

    el = EventLogger()
    el.register_event_schema(schema0)
    with pytest.raises(SchemaRegistryException):
        el.register_event_schema(schema1)


async def test_noop_emit():
    """Tests that the emit method returns
    immediately if no handlers are listeners
    are mapped to the incoming event. This
    is important for performance.
    """
    el = EventLogger()
    # The `emit` method calls `validate_event` if
    # it doesn't return immediately. We'll use the
    # MagicMock here to see if/when this method is called
    # to ensure `emit` is returning when it should.
    el.schemas.validate_event = MagicMock(name="validate_event")  # type:ignore[method-assign]

    schema_id1 = "http://test/test"
    schema1 = {
        "$id": schema_id1,
        "version": 1,
        "type": "object",
        "properties": {
            "something": {
                "type": "string",
                "title": "test",
            },
        },
    }
    schema_id2 = "http://test/test2"
    schema2 = {
        "$id": schema_id2,
        "version": 1,
        "type": "object",
        "properties": {
            "something_elss": {
                "type": "string",
                "title": "test",
            },
        },
    }
    el.register_event_schema(schema1)
    el.register_event_schema(schema2)

    # No handlers or listeners are registered
    # So the validate_event method should not
    # be called.
    el.emit(schema_id=schema_id1, data={"something": "hello"})

    el.schemas.validate_event.assert_not_called()

    # Register a handler and check that .emit
    # validates the method.
    handler = logging.StreamHandler()
    el.register_handler(handler)

    el.emit(schema_id=schema_id1, data={"something": "hello"})

    el.schemas.validate_event.assert_called_once()

    # Reset
    el.remove_handler(handler)
    el.schemas.validate_event.reset_mock()
    assert el.schemas.validate_event.call_count == 0

    # Create a listener and check that emit works

    async def listener(logger: EventLogger, schema_id: str, data: dict) -> None:
        return None

    el.add_listener(schema_id=schema_id1, listener=listener)

    el.emit(schema_id=schema_id1, data={"something": "hello"})

    el.schemas.validate_event.assert_called_once()
    el.schemas.validate_event.reset_mock()
    assert el.schemas.validate_event.call_count == 0

    # Emit a different event with no listeners or
    # handlers and make sure it returns immediately.
    el.emit(schema_id=schema_id2, data={"something_else": "hello again"})
    el.schemas.validate_event.assert_not_called()
