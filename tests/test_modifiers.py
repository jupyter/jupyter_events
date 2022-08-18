import io
import json
import logging

import pytest

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

    def redactor(schema_id: str, version: int, data: dict) -> dict:
        if "username" in data:
            data["username"] = "<masked>"
        return data

    # Add the modifier
    logger.add_modifier(modifier=redactor)

    logger.emit(
        schema_id=schema.id, version=schema.version, data={"username": "jovyan"}
    )
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
        def redact(self, schema_id: str, version: int, data: dict) -> dict:
            if "username" in data:
                data["username"] = "<masked>"
            return data

    redactor = Redactor()

    # Add the modifier
    logger.add_modifier(modifier=redactor.redact)

    logger.emit(
        schema_id=schema.id, version=schema.version, data={"username": "jovyan"}
    )

    # Flush from the handler
    handler.flush()
    # Read from the io
    output = json.loads(sink.getvalue())
    assert "username" in output
    assert output["username"] == "<masked>"


def test_bad_modifier_functions():
    logger = EventLogger()

    def modifier_with_extra_args(
        schema_id: str, version: int, data: dict, unknown_arg: dict
    ) -> dict:
        return data

    with pytest.raises(ModifierError):
        logger.add_modifier(modifier=modifier_with_extra_args)

    # Ensure no modifier was added.
    assert len(logger.modifiers) == 0


def test_bad_modifier_method():
    logger = EventLogger()

    class Redactor:
        def redact(
            self, schema_id: str, version: int, data: dict, extra_args: dict
        ) -> dict:
            return data

    redactor = Redactor()

    with pytest.raises(ModifierError):
        logger.add_modifier(modifier=redactor.redact)

    # Ensure no modifier was added
    assert len(logger.modifiers) == 0


def test_modifier_without_annotations():
    logger = EventLogger()

    def modifier_with_extra_args(event):
        return event

    with pytest.raises(ModifierError):
        logger.add_modifier(modifier=modifier_with_extra_args)
