"""
Emit structured, discrete events when various actions happen.
"""
from traitlets.config import Configurable

import logging
from datetime import datetime
import jsonschema
from pythonjsonlogger import jsonlogger
from traitlets import TraitType, List
import json
import six


class Callable(TraitType):
    """
    A trait which is callable.

    Classes are callable, as are instances
    with a __call__() method.
    """
    info_text = 'a callable'
    def validate(self, obj, value):
        if six.callable(value):
            return value
        else:
            self.error(obj, value)

def _skip_message(record, **kwargs):
    """
    Remove 'message' from log record.

    It is always emitted with 'null', and we do not want it,
    since we are always emitting events only
    """
    del record['message']
    return json.dumps(record, **kwargs)


class EventLog(Configurable):
    """
    Send structured events to a logging sink
    """
    # Traitlets can't take non-pickleable objects, so can't pass in
    # logging handlers directly. This is a temporary hack we should fix?
    handlers_maker = Callable(
        None,
        config=True,
        allow_none=True,
        help="""
        Callable that returns a list of logging.Handler instances to send events to.

        When set to None (the default), events are discarded.
        """
    )

    allowed_schemas = List(
        [],
        config=True,
        help="""
        Fully qualified names of schemas to record.

        Each schema you want to record must be manually specified.
        The default, an empty list, means no events are recorded.
        """
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.log = logging.getLogger(__name__)
        # We don't want events to show up in the default logs
        self.log.propagate = False
        # We will use log.info to emit
        self.log.setLevel(logging.INFO)

        if self.handlers_maker:
            self.handlers = self.handlers_maker(self)
            formatter = jsonlogger.JsonFormatter(json_serializer=_skip_message)
            for handler in self.handlers:
                handler.setFormatter(formatter)
                self.log.addHandler(handler)

        self.schemas = {}

    def register_schema(self, schema):
        """
        Register a given JSON Schema with this event emitter

        'version' and '$id' are required fields.
        """
        # Check if our schema itself is valid
        # This throws an exception if it isn't valid
        jsonschema.validators.validator_for(schema).check_schema(schema)

        # Check that the properties we require are present
        required_schema_fields = {'$id', 'version'}
        for rsf in required_schema_fields:
            if rsf not in schema:
                raise ValueError(
                    '{} is required in schema specification'.format(rsf)
                )

        # Make sure reserved, auto-added fields are not in schema
        if any([p.startswith('__') for p in schema['properties']]):
            raise ValueError(
                'Schema {} has properties beginning with __, which is not allowed'
            )

        self.schemas[(schema['$id'], schema['version'])] = schema

    def record_event(self, schema_name, version, event):
        """
        Record given event with schema has occured.
        """
        if not (self.handlers_maker and schema_name in self.allowed_schemas):
            # if handler isn't set up or schema is not explicitly whitelisted,
            # don't do anything
            return

        if (schema_name, version) not in self.schemas:
            raise ValueError('Schema {schema_name} version {version} not registered'.format(
                schema_name=schema_name, version=version
            ))
        schema = self.schemas[(schema_name, version)]
        jsonschema.validate(event, schema)

        capsule = {
            '__timestamp__': datetime.utcnow().isoformat() + 'Z',
            '__schema__': schema_name,
            '__version__': version
        }
        capsule.update(event)
        self.log.info(capsule)