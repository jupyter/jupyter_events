import json
from pathlib import Path, PurePath
from typing import Tuple, Union

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
            # Path accepts any string, so this
            # won't throw an error if give it
            # a schema string (not a file name). We
            # need to do further checks to ensure this
            # is a file to read from.
            fpath = Path(schema)
            # Check if this is an existing file.
            # If if doesn't exists, it could mean
            # two different things: 1. this is the
            # wrong file path or 2. this is actually
            # a schema in the form of a string.
            if fpath.exists():
                _schema = yaml.load(schema)
            # Try loading this string as a schema object.
            else:
                _schema = yaml.loads(schema)
                # If _schema is still a string (not a schema dict),
                # it means
                if isinstance(_schema, str):
                    raise EventSchemaLoadingError(
                        "We tried reading the `schema` string as a file path, but "
                        "the path did not exist. Then, we tried deserializing the "
                        "`schema` string, but a string was returned where a schema "
                        "dictionary was expected. Please check `schema` to make "
                        "sures it is either a valid file path or schema string."
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

    @property
    def registry_key(self) -> Tuple[str, int]:
        return (self.id, self.version)

    def validate(self, data: dict) -> None:
        """Validate an incoming instance of this event schema."""
        self._validator.validate(data)
