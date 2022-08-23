import pytest

from jupyter_events.logger import EventLogger, ListenerError
from jupyter_events.schema import EventSchema

from .utils import SCHEMA_PATH


@pytest.fixture
def schema():
    # Read schema from path.
    schema_path = SCHEMA_PATH / "good" / "basic.yaml"
    return EventSchema(schema=schema_path)


@pytest.fixture
def event_logger(schema):
    logger = EventLogger()
    logger.register_event_schema(schema)
    return logger


async def test_listener_function(event_logger, schema):
    global listener_was_called
    listener_was_called = False

    async def my_listener(logger: EventLogger, schema_id: str, data: dict) -> None:
        global listener_was_called
        listener_was_called = True  # type: ignore

    # Add the modifier
    event_logger.add_listener(schema_id=schema.id, listener=my_listener)
    event_logger.emit(schema_id=schema.id, data={"prop": "hello, world"})
    await event_logger.gather_listeners()
    assert listener_was_called


def test_bad_listener_function(event_logger, schema):
    logger = EventLogger()

    async def listener_with_extra_args(
        logger: EventLogger, schema_id: str, data: dict, unknown_arg: dict
    ) -> None:
        pass

    with pytest.raises(ListenerError):
        event_logger.add_listener(
            schema_id=schema.id,
            listener=listener_with_extra_args,
        )

    # Ensure no modifier was added.
    assert len(logger._unmodified_listeners) == 0
