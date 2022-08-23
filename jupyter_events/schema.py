import json
from pathlib import PurePath
from typing import Union

from jsonschema import validators
from jsonschema.protocols import Validator

from . import yaml
from .validators import validate_schema


class EventSchemaLoadingError(Exception):
    pass


class EventSchema:
    """A validated schema that can be used.

    On instantiation, validate the schema against
    Jupyter Event's metaschema.

    Parameters
    ----------
    schema: dict or str
        JSON schema to validate against Jupyter Events.

    validator_class: jsonschema.validators
        The validator class from jsonschema used to validate instances
        of this event schema. The schema itself will be validated
        against Jupyter Event's metaschema to ensure that
        any schema registered here follows the expected form
        of Jupyter Events.

    resolver:
        RefResolver for nested JSON schema references.
    """

    def __init__(
        self,
        schema: Union[dict, str, PurePath],
        validator_class: Validator = validators.Draft7Validator,
        resolver=None,
    ):
        _schema = self._load_schema(schema)
        # Validate the schema against Jupyter Events metaschema.
        validate_schema(_schema)
        # Create a validator for this schema
        self._validator = validator_class(_schema, resolver=resolver)
        self._schema = _schema

    def __repr__(self):
        out = f"Validator class: {self._validator.__class__.__name__}\n"
        out += f"Schema: {json.dumps(self._schema, indent=2)}"
        return out

    @staticmethod
    def _load_schema(schema: Union[dict, str, PurePath]) -> dict:
        """Load a JSON schema from different sources/data types.

        `schema` could be a dictionary, string, or pathlib object representing
        a schema file on disk.

        Returns a dictionary with schema data.
        """
        if isinstance(schema, str):
            _schema = yaml.loads(schema)
            if not isinstance(_schema, dict):
                raise EventSchemaLoadingError(
                    "When deserializing `schema`, we expected a dictionary "
                    f"to be returned but a {type(_schema)} was returned "
                    "instead. Double check the `schema` to make sure it "
                    "is in the proper form."
                )
        # Load from a PurePath.
        elif isinstance(schema, PurePath):
            _schema = yaml.load(schema)
        else:
            _schema = schema
        return _schema

    @property
    def id(self) -> str:
        """Schema $id field."""
        return self._schema["$id"]

    @property
    def version(self) -> int:
        """Schema's version."""
        return self._schema["version"]

    def validate(self, data: dict) -> None:
        """Validate an incoming instance of this event schema."""
        self._validator.validate(data)
