import io
import json
import logging

import pytest

from jupyter_events.logger import EventLogger, ModifierError
from jupyter_events.schema import EventSchema

from .utils import SCHEMA_PATH


def test_modifier():
    # Read schema from path.
    schema_path = SCHEMA_PATH / "good" / "user.yaml"
    schema = EventSchema(schema=schema_path)

    sink = io.StringIO()
    handler = logging.StreamHandler(sink)

    logger = EventLogger()
    logger.register_handler(handler)
    logger.register_event_schema(schema)

    def redactor(data: dict = {}) -> dict:
        if "username" in data:
            data["username"] = "<masked>"
        return data

    # Add the modifier
    logger.add_modifier(redactor)

    logger.emit(schema.id, schema.version, {"username": "jovyan"})

    # Flush from the handler
    handler.flush()
    # Read from the io
    output = json.loads(sink.getvalue())
    assert "username" in output
    assert output["username"] == "<masked>"


def test_modifier_class():
    # Read schema from path.
    schema_path = SCHEMA_PATH / "good" / "user.yaml"
    schema = EventSchema(schema=schema_path)

    sink = io.StringIO()
    handler = logging.StreamHandler(sink)

    logger = EventLogger()
    logger.register_handler(handler)
    logger.register_event_schema(schema)

    class Redactor:
        def redact(self, data: dict) -> dict:
            if "username" in data:
                data["username"] = "<masked>"
            return data

    redactor = Redactor()

    # Add the modifier
    logger.add_modifier(redactor.redact)

    logger.emit(schema.id, schema.version, {"username": "jovyan"})

    # Flush from the handler
    handler.flush()
    # Read from the io
    output = json.loads(sink.getvalue())
    assert "username" in output
    assert output["username"] == "<masked>"


def test_bad_modifier():
    logger = EventLogger()
    # Add a bad modifier

    def bad_modifier(data: dict, unknown_arg: dict) -> dict:
        return data

    with pytest.raises(ModifierError):
        logger.add_modifier(bad_modifier)

    def bad_modifier_2(data: bool) -> dict:
        pass

    with pytest.raises(ModifierError):
        logger.add_modifier(bad_modifier_2)

    class Redactor:
        def redact(self, data: dict, extra_args: dict) -> dict:
            if "username" in data:
                data["username"] = "<masked>"
            return data

    redactor = Redactor()

    with pytest.raises(ModifierError):
        logger.add_modifier(redactor.redact)
