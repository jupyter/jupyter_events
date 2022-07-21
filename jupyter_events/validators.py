import pathlib

from jsonschema import RefResolver, ValidationError, validators

from . import yaml

METASCHEMA_PATH = pathlib.Path(__file__).parent.joinpath("schemas")
EVENT_METASCHEMA_FILEPATH = METASCHEMA_PATH.joinpath("event-metaschema.yml")
EVENT_METASCHEMA = yaml.load(EVENT_METASCHEMA_FILEPATH)
PROPERTY_METASCHEMA_FILEPATH = METASCHEMA_PATH.joinpath("property-metaschema.yml")
PROPERTY_METASCHEMA = yaml.load(PROPERTY_METASCHEMA_FILEPATH)
SCHEMA_STORE = {
    PROPERTY_METASCHEMA["$id"]: PROPERTY_METASCHEMA,
}
METASCHEMA_RESOLVER = RefResolver(
    base_uri=EVENT_METASCHEMA["$id"], referrer=EVENT_METASCHEMA, store=SCHEMA_STORE
)
JUPYTER_EVENTS_VALIDATOR = validators.Draft202012Validator(
    schema=EVENT_METASCHEMA, resolver=METASCHEMA_RESOLVER
)


def validate_schema(schema: dict):
    try:
        # Validate the schema against Jupyter Events metaschema.
        JUPYTER_EVENTS_VALIDATOR.validate(schema)
    except ValidationError as err:
        reserved_property_msg = " does not match '^(?!__.*)'"
        if reserved_property_msg in str(err):
            bad_property = str(err)[: -(len(reserved_property_msg))]
            raise ValidationError(
                f"{bad_property} is an invalid property name because it "
                "starts with `__`. Properties starting with 'dunder' "
                "are reserved for Jupyter Events."
            )
        raise err
