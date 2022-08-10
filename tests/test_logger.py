import io
import json
import logging
from datetime import datetime, timedelta

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
    cfg = loader.load_config()
    return cfg


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
        "$id": "test/test",
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

    timestamp_override = datetime.utcnow() - timedelta(days=1)
    el.emit(
        "test/test", 1, {"something": "blah"}, timestamp_override=timestamp_override
    )
    handler.flush()
    event_capsule = json.loads(output.getvalue())
    assert event_capsule["__timestamp__"] == timestamp_override.isoformat() + "Z"


def test_emit():
    """
    Simple test for emitting valid events
    """
    schema = {
        "$id": "test/test",
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

    el.emit(
        "test/test",
        1,
        {
            "something": "blah",
        },
    )
    handler.flush()

    event_capsule = json.loads(output.getvalue())

    assert "__timestamp__" in event_capsule
    # Remove timestamp from capsule when checking equality, since it is gonna vary
    del event_capsule["__timestamp__"]
    assert event_capsule == {
        "__schema__": "test/test",
        "__schema_version__": 1,
        "__metadata_version__": 1,
        "something": "blah",
    }


def test_register_event_schema(tmp_path):
    """
    Register schema from a file
    """
    schema = {
        "$id": "test/test",
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
    assert ("test/test", 1) in el.schemas


def test_register_event_schema_object(tmp_path):
    """
    Register schema from a file
    """
    schema = {
        "$id": "test/test",
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

    assert ("test/test", 1) in el.schemas


def test_emit_badschema():
    """
    Fail fast when an event doesn't conform to its schema
    """
    schema = {
        "$id": "test/test",
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
    el.allowed_schemas = ["test/test"]

    with pytest.raises(jsonschema.ValidationError):
        el.emit("test/test", 1, {"something": "blah", "status": "hi"})  # 'not-in-enum'


def test_unique_logger_instances():
    schema0 = {
        "$id": "test/test0",
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
        "$id": "test/test1",
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
    el0.allowed_schemas = ["test/test0"]

    el1 = EventLogger(handlers=[handler1])
    el1.register_event_schema(schema1)
    el1.allowed_schemas = ["test/test1"]

    el0.emit(
        "test/test0",
        1,
        {
            "something": "blah",
        },
    )
    el1.emit(
        "test/test1",
        1,
        {
            "something": "blah",
        },
    )
    handler0.flush()
    handler1.flush()

    event_capsule0 = json.loads(output0.getvalue())

    assert "__timestamp__" in event_capsule0
    # Remove timestamp from capsule when checking equality, since it is gonna vary
    del event_capsule0["__timestamp__"]
    assert event_capsule0 == {
        "__schema__": "test/test0",
        "__schema_version__": 1,
        "__metadata_version__": 1,
        "something": "blah",
    }

    event_capsule1 = json.loads(output1.getvalue())

    assert "__timestamp__" in event_capsule1
    # Remove timestamp from capsule when checking equality, since it is gonna vary
    del event_capsule1["__timestamp__"]
    assert event_capsule1 == {
        "__schema__": "test/test1",
        "__schema_version__": 1,
        "__metadata_version__": 1,
        "something": "blah",
    }


def test_register_duplicate_schemas():
    schema0 = {
        "$id": "test/test",
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
        "$id": "test/test",
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
