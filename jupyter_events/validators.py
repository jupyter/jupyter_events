import pathlib

from jsonschema import RefResolver, validators

from .yaml import yaml

METASCHEMA_PATH = pathlib.Path(__file__).parent.joinpath("schemas")
EVENT_METASCHEMA_FILEPATH = METASCHEMA_PATH.joinpath("event-metaschema.yml")
EVENT_METASCHEMA = yaml.load(EVENT_METASCHEMA_FILEPATH)
PROPERTY_METASCHEMA_FILEPATH = METASCHEMA_PATH.joinpath("property-metaschema.yml")
PROPERTY_METASCHEMA = yaml.load(PROPERTY_METASCHEMA_FILEPATH)
RESERVED_PROPERTY_METASCHEMA_FILEPATH = METASCHEMA_PATH.joinpath(
    "reserved-property-metaschema.yml"
)
RESERVED_PROPERTY_METASCHEMA = yaml.load(RESERVED_PROPERTY_METASCHEMA_FILEPATH)
METASCHEMA_RESOLVER = RefResolver(
    base_uri=EVENT_METASCHEMA["$id"],
    referrer=EVENT_METASCHEMA,
    store={
        PROPERTY_METASCHEMA["$id"]: PROPERTY_METASCHEMA,
        RESERVED_PROPERTY_METASCHEMA["$id"]: RESERVED_PROPERTY_METASCHEMA,
    },
)
JUPYTER_EVENTS_VALIDATOR = validators.Draft7Validator(
    EVENT_METASCHEMA, resolver=METASCHEMA_RESOLVER
)
