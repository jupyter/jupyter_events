"""
Emit structured, discrete events when various actions happen.
"""
import json
import logging
import warnings
from datetime import datetime
from pathlib import PurePath
from typing import Union

from pythonjsonlogger import jsonlogger
from traitlets import Instance, default
from traitlets.config import Config, Configurable

from . import EVENTS_METADATA_VERSION
from .schema_registry import SchemaRegistry
from .traits import Handlers


class SchemaNotRegistered(Warning):
    """A warning to raise when an event is given to the logger
    but its schema has not be registered with the EventLogger
    """


# Only show this warning on the first instance
# of each event type that fails to emit.
warnings.simplefilter("once", SchemaNotRegistered)


class EventLogger(Configurable):
    """
    An Event logger for emitting structured events.

    Event schemas must be registered with the
    EventLogger using the `register_schema` or
    `register_schema_file` methods. Every schema
    will be validated against Jupyter Event's metaschema.
    """

    handlers = Handlers(
        default_value=[],
        allow_none=True,
        help="""A list of logging.Handler instances to send events to.

        When set to None (the default), all events are discarded.
        """,
    ).tag(config=True)

    schemas = Instance(
        SchemaRegistry,
        help="""The SchemaRegistry for caching validated schemas
        and their jsonschema validators.
        """,
    )

    @default("schemas")
    def _default_schemas(self) -> SchemaRegistry:
        return SchemaRegistry()

    def __init__(self, *args, **kwargs):
        # We need to initialize the configurable before
        # adding the logging handlers.
        super().__init__(*args, **kwargs)
        # Use a unique name for the logger so that multiple instances of EventLog do not write
        # to each other's handlers.
        log_name = __name__ + "." + str(id(self))
        self.log = logging.getLogger(log_name)
        # We don't want events to show up in the default logs
        self.log.propagate = False
        # We will use log.info to emit
        self.log.setLevel(logging.INFO)
        # Add each handler to the logger and format the handlers.
        if self.handlers:
            for handler in self.handlers:
                self.register_handler(handler)

    def _load_config(self, cfg, section_names=None, traits=None):
        """Load EventLogger traits from a Config object, patching the
        handlers trait in the Config object to avoid deepcopy errors.
        """
        my_cfg = self._find_my_config(cfg)
        handlers = my_cfg.pop("handlers", [])

        # Turn handlers list into a pickeable function
        def get_handlers():
            return handlers

        my_cfg["handlers"] = get_handlers

        # Build a new eventlog config object.
        eventlogger_cfg = Config({"EventLogger": my_cfg})
        super()._load_config(eventlogger_cfg, section_names=None, traits=None)

    def register_event_schema(self, schema: Union[dict, str, PurePath]):
        """Register this schema with the schema registry.

        Get this registered schema using the EventLogger.schema.get() method.
        """
        self.schemas.register(schema)

    def register_handler(self, handler: logging.Handler):
        """Register a new logging handler to the Event Logger.

        All outgoing messages will be formatted as a JSON string.
        """

        def _skip_message(record, **kwargs):
            """
            Remove 'message' from log record.
            It is always emitted with 'null', and we do not want it,
            since we are always emitting events only
            """
            del record["message"]
            return json.dumps(record, **kwargs)

        formatter = jsonlogger.JsonFormatter(json_serializer=_skip_message)
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
        if handler not in self.handlers:
            self.handlers.append(handler)

    def remove_handler(self, handler: logging.Handler):
        """Remove a logging handler from the logger and list of handlers."""
        self.log.removeHandler(handler)
        if handler in self.handlers:
            self.handlers.remove(handler)

    def emit(self, schema_id: str, version: int, data: dict, timestamp_override=None):
        """
        Record given event with schema has occurred.

        Parameters
        ----------
        schema_id: str
            $id of the schema
        version: str
            The schema version
        event: dict
            The event to record
        timestamp_override: datetime, optional
            Optionally override the event timestamp. By default it is set to the current timestamp.

        Returns
        -------
        dict
            The recorded event data
        """
        # If no handlers are routing these events, there's no need to proceed.
        if not self.handlers:
            return

        # If the schema hasn't been registered, raise a warning to make sure
        # this was intended.
        if (schema_id, version) not in self.schemas:
            warnings.warn(
                f"({schema_id}, {version}) has not been registered yet. If "
                "this was not intentional, please register the schema using the "
                "`register_event_schema` method.",
                SchemaNotRegistered,
            )
            return

        # Generate the empty event capsule.
        if timestamp_override is None:
            timestamp = datetime.utcnow()
        else:
            timestamp = timestamp_override
        capsule = {
            "__timestamp__": timestamp.isoformat() + "Z",
            "__schema__": schema_id,
            "__schema_version__": version,
            "__metadata_version__": EVENTS_METADATA_VERSION,
        }
        # Process this event, i.e. validate and redact (in place)
        self.schemas.validate_event(schema_id, version, data)
        capsule.update(data)
        self.log.info(capsule)
        return capsule
