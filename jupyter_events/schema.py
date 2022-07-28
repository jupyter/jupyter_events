from typing import Any, Dict, Hashable, List, Sequence, Tuple, Union

from jsonschema import validators

from . import yaml
from .validators import validate_schema


class EventSchema:
    """A validated schema that can be used.

    On instantiation, validate the schema against
    Jupyter Event's metaschema.

    Parameters
    ----------
    schema: dict
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
        schema,
        validator_class=validators.Draft7Validator,
        resolver=None,
    ):
        # Validate the schema against Jupyter Events metaschema.
        validate_schema(schema)
        # Create a validator for this schema
        self._validator = validator_class(schema, resolver=resolver)
        self._schema = schema

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
