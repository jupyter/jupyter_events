import io
import json
import logging

import pytest

from jupyter_events import Event
from jupyter_events.dataclasses import ModifierData
from jupyter_events.logger import EventLogger, ModifierError
from jupyter_events.schema import EventSchema

from .utils import SCHEMA_PATH


def test_modifier_function():
    # Read schema from path.
    schema_path = SCHEMA_PATH / "good" / "user.yaml"
    schema = EventSchema(schema=schema_path)

    sink = io.StringIO()
    handler = logging.StreamHandler(sink)

    logger = EventLogger()
    logger.register_handler(handler)
    logger.register_event_schema(schema)

    def redactor(data: ModifierData) -> dict:
        d = data.event_data
        if "username" in d:
            d["username"] = "<masked>"
        return d

    # Add the modifier
    logger.add_modifier(redactor)

    logger.emit(Event(schema.id, schema.version, {"username": "jovyan"}))
    # Flush from the handler
    handler.flush()
    # Read from the io
    output = json.loads(sink.getvalue())
    assert "username" in output
    assert output["username"] == "<masked>"


def test_modifier_method():
    # Read schema from path.
    schema_path = SCHEMA_PATH / "good" / "user.yaml"
    schema = EventSchema(schema=schema_path)

    sink = io.StringIO()
    handler = logging.StreamHandler(sink)

    logger = EventLogger()
    logger.register_handler(handler)
    logger.register_event_schema(schema)

    class Redactor:
        def redact(self, data: ModifierData) -> dict:
            d = data.event_data
            if "username" in d:
                d["username"] = "<masked>"
            return d

    redactor = Redactor()

    # Add the modifier
    logger.add_modifier(redactor.redact)

    logger.emit(Event(schema.id, schema.version, {"username": "jovyan"}))

    # Flush from the handler
    handler.flush()
    # Read from the io
    output = json.loads(sink.getvalue())
    assert "username" in output
    assert output["username"] == "<masked>"


def test_bad_modifier_functions():
    logger = EventLogger()

    def modifier_with_extra_args(data: ModifierData, unknown_arg: dict) -> dict:
        return data.event_data

    with pytest.raises(ModifierError):
        logger.add_modifier(modifier_with_extra_args)

    # Ensure no modifier was added.
    assert len(logger.modifiers) == 0

    def modifier_with_few_args(data: bool) -> dict:
        pass

    with pytest.raises(ModifierError):
        logger.add_modifier(modifier_with_few_args)

    # Ensure no modifier was added
    assert len(logger.modifiers) == 0


def test_bad_modifier_method():
    logger = EventLogger()

    class Redactor:
        def redact(self, data: ModifierData, extra_args: dict) -> dict:
            d = data.event_data
            if "username" in d:
                d["username"] = "<masked>"
            return d

    redactor = Redactor()

    with pytest.raises(ModifierError):
        logger.add_modifier(redactor.redact)

    # Ensure no modifier was added
    assert len(logger.modifiers) == 0


def test_modifier_without_annotations():
    logger = EventLogger()

    def modifier_with_extra_args(data):
        return data

    with pytest.raises(ModifierError):
        logger.add_modifier(modifier_with_extra_args)
