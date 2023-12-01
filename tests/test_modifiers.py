from __future__ import annotations

import pytest

from jupyter_events.schema import EventSchema

from .utils import SCHEMA_PATH


@pytest.fixture
def schema():
    # Read schema from path.
    schema_path = SCHEMA_PATH / "good" / "user.yaml"
    return EventSchema(schema=schema_path)


@pytest.fixture
def jp_event_schemas(schema):
    return [schema]


def test_modifier_function(schema, jp_event_logger, jp_read_emitted_events):
    event_logger = jp_event_logger

    def redactor(schema_id: str, data: dict) -> dict:
        if "username" in data:
            data["username"] = "<masked>"
        return data

    # Add the modifier
    event_logger.add_modifier(modifier=redactor)
    event_logger.emit(schema_id=schema.id, data={"username": "jovyan"})
    output = jp_read_emitted_events()[0]
    assert "username" in output
    assert output["username"] == "<masked>"


def test_modifier_method(schema, jp_event_logger, jp_read_emitted_events):
    event_logger = jp_event_logger

    class Redactor:
        def redact(self, schema_id: str, data: dict) -> dict:
            if "username" in data:
                data["username"] = "<masked>"
            return data

    redactor = Redactor()

    # Add the modifier
    event_logger.add_modifier(modifier=redactor.redact)

    event_logger.emit(schema_id=schema.id, data={"username": "jovyan"})
    output = jp_read_emitted_events()[0]
    assert "username" in output
    assert output["username"] == "<masked>"


def test_remove_modifier(schema, jp_event_logger, jp_read_emitted_events):
    event_logger = jp_event_logger

    def redactor(schema_id: str, data: dict) -> dict:
        if "username" in data:
            data["username"] = "<masked>"
        return data

    # Add the modifier
    event_logger.add_modifier(modifier=redactor)

    assert len(event_logger._modifiers) == 1

    event_logger.emit(schema_id=schema.id, data={"username": "jovyan"})
    output = jp_read_emitted_events()[0]

    assert "username" in output
    assert output["username"] == "<masked>"

    event_logger.remove_modifier(modifier=redactor)

    event_logger.emit(schema_id=schema.id, data={"username": "jovyan"})
    output = jp_read_emitted_events()[0]

    assert "username" in output
    assert output["username"] == "jovyan"
