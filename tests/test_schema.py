from __future__ import annotations

import os
from pathlib import Path

import pytest
from jsonschema.exceptions import ValidationError

from jupyter_events import yaml
from jupyter_events.schema import (
    EventSchema,
    EventSchemaFileAbsent,
    EventSchemaLoadingError,
    EventSchemaUnrecognized,
)
from jupyter_events.validators import validate_schema

from .utils import SCHEMA_PATH

BAD_SCHEMAS = [
    ["reserved-property.yaml", "Properties starting with 'dunder'"],
    ["nested-reserved-property.yaml", "Properties starting with 'dunder'"],
    ["bad-id.yaml", "'not-a-uri' is not a 'uri'"],
]

GOOD_SCHEMAS = ["array.yaml", "nested-array.yaml", "basic.yaml"]


@pytest.mark.parametrize("schema_file,validation_error_msg", BAD_SCHEMAS)
def test_bad_validations(schema_file, validation_error_msg):
    """
    Validation fails because the schema is missing
    a redactionPolicies field.
    """
    # Read the schema file
    with Path.open(SCHEMA_PATH / "bad" / schema_file) as f:
        schema = yaml.loads(f)
    # Assert that the schema files for a known reason.
    with pytest.raises(ValidationError) as err:
        validate_schema(schema)
    assert validation_error_msg in err.value.message


def test_file_absent():
    """Validation fails because file does not exist at path."""
    with pytest.raises(EventSchemaFileAbsent):
        EventSchema(Path("asdf.txt"))


def test_string_intended_as_path():
    """Ensure EventSchema returns a helpful error message if user passes a
    string intended as a Path."""
    expected_msg_contents = "Paths to schema files must be explicitly wrapped in a Pathlib object."
    str_path = os.path.join(SCHEMA_PATH, "good", "some_schema.yaml")  # noqa: PTH118
    with pytest.raises(EventSchemaLoadingError) as e:
        EventSchema(str_path)

    assert expected_msg_contents in str(e)


def test_unrecognized_type():
    """Validation fails because file is not of valid type."""
    with pytest.raises(EventSchemaUnrecognized):
        EventSchema(9001)  # type:ignore[arg-type]


def test_invalid_yaml():
    """Validation fails because deserialized schema is not a dictionary."""
    path = SCHEMA_PATH / "bad" / "invalid.yaml"
    with pytest.raises(EventSchemaLoadingError):
        EventSchema(path)


def test_valid_json():
    """Ensure EventSchema accepts JSON files."""
    path = SCHEMA_PATH / "good" / "basic.json"
    EventSchema(path)


@pytest.mark.parametrize("schema_file", GOOD_SCHEMAS)
def test_good_validations(schema_file):
    """Ensure validation passes for good schemas."""
    # Read the schema file
    with Path.open(SCHEMA_PATH / "good" / schema_file) as f:
        schema = yaml.loads(f)
    # assert that no exception gets raised
    validate_schema(schema)


@pytest.mark.parametrize(
    "schema",
    [
        # Non existent paths
        "non-existent-file.yml",
        "non/existent/path",
        "non/existent/path/file.yaml",
        # Valid yaml string, but not a valid object
        "random string",
    ],
)
def test_loading_string_error(schema):
    with pytest.raises(EventSchemaLoadingError):
        EventSchema(schema)
