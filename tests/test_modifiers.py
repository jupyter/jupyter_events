import io
import json
import logging

import pytest

from jupyter_events.logger import EventLogger, ModifierError
from jupyter_events.schema import EventSchema

from .utils import SCHEMA_PATH


@pytest.fixture
def sink():
    return io.StringIO()


@pytest.fixture
def schema():
    # Read schema from path.
    schema_path = SCHEMA_PATH / "good" / "user.yaml"
    return EventSchema(schema=schema_path)


@pytest.fixture
def handler(sink):
    return logging.StreamHandler(sink)


@pytest.fixture
def event_logger(handler, schema):
    logger = EventLogger()
    logger.register_handler(handler)
    logger.register_event_schema(schema)
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


def test_modifier_function(schema, event_logger, read_emitted_event):
    def redactor(schema_id: str, data: dict) -> dict:
        if "username" in data:
            data["username"] = "<masked>"
        return data

    # Add the modifier
    event_logger.add_modifier(modifier=redactor)
    event_logger.emit(schema_id=schema.id, data={"username": "jovyan"})
    output = read_emitted_event()
    assert "username" in output
    assert output["username"] == "<masked>"


def test_modifier_method(schema, event_logger, read_emitted_event):
    class Redactor:
        def redact(self, schema_id: str, data: dict) -> dict:
            if "username" in data:
                data["username"] = "<masked>"
            return data

    redactor = Redactor()

    # Add the modifier
    event_logger.add_modifier(modifier=redactor.redact)

    event_logger.emit(schema_id=schema.id, data={"username": "jovyan"})
    output = read_emitted_event()
    assert "username" in output
    assert output["username"] == "<masked>"


def test_bad_modifier_functions(event_logger, schema: EventSchema):
    def modifier_with_extra_args(schema_id: str, data: dict, unknown_arg: dict) -> dict:
        return data

    with pytest.raises(ModifierError):
        event_logger.add_modifier(modifier=modifier_with_extra_args)

    # Ensure no modifier was added.
    assert len(event_logger._modifiers[schema.id]) == 0


def test_bad_modifier_method(event_logger, schema: EventSchema):
    class Redactor:
        def redact(self, schema_id: str, data: dict, extra_args: dict) -> dict:
            return data

    redactor = Redactor()

    with pytest.raises(ModifierError):
        event_logger.add_modifier(modifier=redactor.redact)

    # Ensure no modifier was added
    assert len(event_logger._modifiers[schema.id]) == 0


def test_modifier_without_annotations():
    logger = EventLogger()

    def modifier_with_extra_args(event):
        return event

    with pytest.raises(ModifierError):
        logger.add_modifier(modifier=modifier_with_extra_args)


def test_remove_modifier(schema, event_logger, read_emitted_event):
    def redactor(schema_id: str, data: dict) -> dict:
        if "username" in data:
            data["username"] = "<masked>"
        return data

    # Add the modifier
    event_logger.add_modifier(modifier=redactor)

    assert len(event_logger._modifiers) == 1

    event_logger.emit(schema_id=schema.id, data={"username": "jovyan"})
    output = read_emitted_event()

    assert "username" in output
    assert output["username"] == "<masked>"

    event_logger.remove_modifier(modifier=redactor)

    event_logger.emit(schema_id=schema.id, data={"username": "jovyan"})
    output = read_emitted_event()

    assert "username" in output
    assert output["username"] == "jovyan"
