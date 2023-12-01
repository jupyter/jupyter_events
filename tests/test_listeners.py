from __future__ import annotations

import io
import logging

import pytest

from jupyter_events.logger import EventLogger
from jupyter_events.schema import EventSchema

from .utils import SCHEMA_PATH


@pytest.fixture
def schema():
    # Read schema from path.
    schema_path = SCHEMA_PATH / "good" / "basic.yaml"
    return EventSchema(schema=schema_path)


@pytest.fixture
def jp_event_schemas(schema):
    return [schema]


async def test_listener_function(jp_event_logger, schema):
    event_logger = jp_event_logger
    listener_was_called = False

    async def my_listener(logger: EventLogger, schema_id: str, data: dict) -> None:
        nonlocal listener_was_called
        listener_was_called = True

    # Add the modifier
    event_logger.add_listener(schema_id=schema.id, listener=my_listener)
    event_logger.emit(schema_id=schema.id, data={"prop": "hello, world"})
    await event_logger.gather_listeners()
    assert listener_was_called
    # Check that the active listeners are cleaned up.
    assert len(event_logger._active_listeners) == 0


async def test_listener_function_str_annotations(jp_event_logger, schema):
    event_logger = jp_event_logger
    listener_was_called = False

    async def my_listener(logger: EventLogger, schema_id: str, data: dict) -> None:
        nonlocal listener_was_called
        listener_was_called = True

    # Add the modifier
    event_logger.add_listener(schema_id=schema.id, listener=my_listener)
    event_logger.emit(schema_id=schema.id, data={"prop": "hello, world"})
    await event_logger.gather_listeners()
    assert listener_was_called
    # Check that the active listeners are cleaned up.
    assert len(event_logger._active_listeners) == 0


async def test_remove_listener_function(jp_event_logger, schema):
    event_logger = jp_event_logger
    listener_was_called = False

    async def my_listener(logger: EventLogger, schema_id: str, data: dict) -> None:
        nonlocal listener_was_called
        listener_was_called = True

    # Add the modifier
    event_logger.add_listener(schema_id=schema.id, listener=my_listener)
    event_logger.emit(schema_id=schema.id, data={"prop": "hello, world"})
    await event_logger.gather_listeners()
    assert listener_was_called

    # Check that the active listeners are cleaned up.
    assert len(event_logger._active_listeners) == 0

    event_logger.remove_listener(listener=my_listener)
    assert len(event_logger._modified_listeners[schema.id]) == 0
    assert len(event_logger._unmodified_listeners[schema.id]) == 0


async def test_listener_that_raises_exception(jp_event_logger, schema):
    event_logger = jp_event_logger

    # Get an application logger that will show the exception
    app_log = event_logger.log
    log_stream = io.StringIO()
    h = logging.StreamHandler(log_stream)
    app_log.addHandler(h)

    async def listener_raise_exception(logger: EventLogger, schema_id: str, data: dict) -> None:
        raise Exception("This failed")  # noqa

    event_logger.add_listener(schema_id=schema.id, listener=listener_raise_exception)
    event_logger.emit(schema_id=schema.id, data={"prop": "hello, world"})

    await event_logger.gather_listeners()

    # Check that the exception was printed to the logs
    h.flush()
    log_output = log_stream.getvalue()
    assert "This failed" in log_output
    # Check that the active listeners are cleaned up.
    assert len(event_logger._active_listeners) == 0


async def test_bad_listener_does_not_break_good_listener(jp_event_logger, schema):
    event_logger = jp_event_logger

    # Get an application logger that will show the exception
    app_log = event_logger.log
    log_stream = io.StringIO()
    h = logging.StreamHandler(log_stream)
    app_log.addHandler(h)

    listener_was_called = False

    async def listener_raise_exception(logger: EventLogger, schema_id: str, data: dict) -> None:
        raise Exception("This failed")  # noqa

    async def my_listener(logger: EventLogger, schema_id: str, data: dict) -> None:
        nonlocal listener_was_called
        listener_was_called = True

    # Add a bad listener and a good listener and ensure that
    # emitting still works and the bad listener's exception is is logged.
    event_logger.add_listener(schema_id=schema.id, listener=listener_raise_exception)
    event_logger.add_listener(schema_id=schema.id, listener=my_listener)

    event_logger.emit(schema_id=schema.id, data={"prop": "hello, world"})

    await event_logger.gather_listeners()

    # Check that the exception was printed to the logs
    h.flush()
    log_output = log_stream.getvalue()
    assert "This failed" in log_output
    assert listener_was_called
    # Check that the active listeners are cleaned up.
    assert len(event_logger._active_listeners) == 0
