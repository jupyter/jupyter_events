"""
Emit structured, discrete events when various actions happen.
"""
import json
import logging
from datetime import datetime

from pythonjsonlogger import jsonlogger

try:
    from ruamel.yaml import YAML
except ImportError as e:
    # check for known conda bug that prevents
    # pip from installing ruamel.yaml dependency
    try:
        import ruamel_yaml  # noqa
    except ImportError:
        # nope, regular import error; raise original
        raise e
    else:
        # have conda fork ruamel_yaml, but not ruamel.yaml.
        # this is a bug in the ruamel_yaml conda package
        # mistakenly identifying itself as ruamel.yaml to pip.
        # conda install the 'real' ruamel.yaml to fix
        raise ImportError(
            "Missing dependency ruamel.yaml. Try: `conda install ruamel.yaml`"
        )

from traitlets.config import Config, Configurable

from . import EVENTS_METADATA_VERSION
from .categories import JSONSchemaValidator, filter_categories_from_event
from .traits import Handlers, SchemaOptions

yaml = YAML(typ="safe")


def _skip_message(record, **kwargs):
    """
    Remove 'message' from log record.
    It is always emitted with 'null', and we do not want it,
    since we are always emitting events only
    """
    del record["message"]
    return json.dumps(record, **kwargs)


class EventLogger(Configurable):
    """
    Send structured events to a logging sink
    """

    handlers = Handlers(
        [],
        allow_none=True,
        help="""A list of logging.Handler instances to send events to.

        When set to None (the default), events are discarded.
        """,
    ).tag(config=True)

    allowed_schemas = SchemaOptions(
        {},
        allow_none=True,
        help="""
        Fully qualified names of schemas to record.

        Each schema you want to record must be manually specified.
        The default, an empty list, means no events are recorded.
        """,
    ).tag(config=True)

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
        self.schemas = {}
        # Add each handler to the logger and format the handlers.
        if self.handlers:
            formatter = jsonlogger.JsonFormatter(json_serializer=_skip_message)
            for handler in self.handlers:
                handler.setFormatter(formatter)
                self.log.addHandler(handler)

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

    def register_schema_file(self, filename):
        """
        Convenience function for registering a JSON schema from a filepath

        Supports both JSON & YAML files.

        Parameters
        ----------
        filename: str, path object or file-like object
            Path to the schema file or a file object to register.
        """
        # Just use YAML loader for everything, since all valid JSON is valid YAML

        # check if input is a file-like object
        if hasattr(filename, "read") and hasattr(filename, "write"):
            self.register_schema(yaml.load(filename))
        else:
            with open(filename) as f:
                self.register_schema(yaml.load(f))

    def register_schema(self, schema):
        """
        Register a given JSON Schema with this event emitter

        'version' and '$id' are required fields.
        """
        # Check if our schema itself is valid
        # This throws an exception if it isn't valid
        JSONSchemaValidator.check_schema(schema)

        # Check that the properties we require are present
        required_schema_fields = {"$id", "version", "properties"}
        for rsf in required_schema_fields:
            if rsf not in schema:
                raise ValueError(f"{rsf} is required in schema specification")

        if (schema["$id"], schema["version"]) in self.schemas:
            raise ValueError(
                "Schema {} version {} has already been registered.".format(
                    schema["$id"], schema["version"]
                )
            )

        for p, attrs in schema["properties"].items():
            if p.startswith("__"):
                raise ValueError(
                    "Schema {} has properties beginning with __, which is not allowed"
                )

            # Validate "categories" property in proposed schema.
            try:
                cats = attrs["categories"]
                # Categories must be a list.
                if not isinstance(cats, list):
                    raise ValueError(
                        'The "categories" field in a registered schemas must be a list.'
                    )
            except KeyError:
                raise KeyError(
                    'All properties must have a "categories" field that describes '
                    'the type of data being collected. The "{}" property does not '
                    "have a category field.".format(p)
                )

        self.schemas[(schema["$id"], schema["version"])] = schema

    def get_allowed_properties(self, schema_name):
        """Get the allowed properties for an allowed schema."""
        config = self.allowed_schemas[schema_name]
        try:
            return set(config["allowed_properties"])
        except KeyError:
            return set()

    def get_allowed_categories(self, schema_name):
        """
        Return a set of allowed categories for a given schema
        from the EventLog's config.
        """
        config = self.allowed_schemas[schema_name]
        try:
            allowed_categories = config["allowed_categories"]
            allowed_categories.append("unrestricted")
            return set(allowed_categories)
        except KeyError:
            return {"unrestricted"}

    def record_event(self, schema_name, version, event, timestamp_override=None):
        """
        Record given event with schema has occurred.

        Parameters
        ----------
        schema_name: str
            Name of the schema
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
        if not (self.handlers and schema_name in self.allowed_schemas):
            # if handler isn't set up or schema is not explicitly whitelisted,
            # don't do anything
            return

        if (schema_name, version) not in self.schemas:
            raise ValueError(
                "Schema {schema_name} version {version} not registered".format(
                    schema_name=schema_name, version=version
                )
            )

        schema = self.schemas[(schema_name, version)]

        # Validate the event data.
        JSONSchemaValidator(schema).validate(event)

        # Generate the empty event capsule.
        if timestamp_override is None:
            timestamp = datetime.utcnow()
        else:
            timestamp = timestamp_override
        capsule = {
            "__timestamp__": timestamp.isoformat() + "Z",
            "__schema__": schema_name,
            "__schema_version__": version,
            "__metadata_version__": EVENTS_METADATA_VERSION,
        }

        # Filter properties in the incoming event based on the
        # allowed categories and properties from the eventlog config.
        allowed_categories = self.get_allowed_categories(schema_name)
        allowed_properties = self.get_allowed_properties(schema_name)

        filtered_event = filter_categories_from_event(
            event, schema, allowed_categories, allowed_properties
        )
        capsule.update(filtered_event)

        self.log.info(capsule)
        return capsule
