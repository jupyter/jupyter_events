import json
from typing import Tuple, Union

from jsonschema import validators
from jsonschema.protocols import Validator

from . import yaml
from .validators import validate_schema


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
        schema: Union[dict, str],
        validator_class: Validator = validators.Draft7Validator,
        resolver=None,
    ):
        # Handle the instance where schema is a string.
        if isinstance(schema, str):
            _schema: dict = yaml.loads(schema)
        else:
            _schema = schema
        # Validate the schema against Jupyter Events metaschema.
        validate_schema(_schema)
        # Create a validator for this schema
        self._validator = validator_class(schema, resolver=resolver)
        self._schema = _schema

    def __repr__(self):
        out = f"Validator class: {self._validator.__class__.__name__}\n"
        out += f"Schema: {json.dumps(self._schema, indent=2)}"
        return out

    @property
    def id(self) -> str:
        """Schema $id field."""
        return self._schema["$id"]

    @property
    def version(self) -> int:
        """Schema's version."""
        return self._schema["version"]

    @property
    def registry_key(self) -> Tuple[str, int]:
        return (self.id, self.version)

    @classmethod
    def from_file(
        cls,
        filepath,
        validator_class=validators.Draft7Validator,
        resolver=None,
    ):
        schema = yaml.load(filepath)
        return cls(
            schema=schema,
            validator_class=validator_class,
            resolver=resolver,
        )

    def validate(self, data: dict) -> None:
        """Validate an incoming instance of this event schema."""
        self._validator.validate(data)
