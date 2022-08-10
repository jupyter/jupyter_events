import pytest
from jsonschema.exceptions import ValidationError

from jupyter_events import yaml
from jupyter_events.schema import EventSchema, EventSchemaLoadingError
from jupyter_events.validators import validate_schema

from .utils import SCHEMA_PATH

BAD_SCHEMAS = [
    ["reserved-property.yaml", "Properties starting with 'dunder'"],
    ["nested-reserved-property.yaml", "Properties starting with 'dunder'"],
]


@pytest.mark.parametrize("schema_file,validation_error_msg", BAD_SCHEMAS)
def test_bad_validations(schema_file, validation_error_msg):
    """
    Validation fails because the schema is missing
    a redactionPolicies field.
    """
    # Read the schema file
    with open(SCHEMA_PATH / "bad" / schema_file) as f:
        schema = yaml.loads(f)
    # Assert that the schema files for a known reason.
    with pytest.raises(ValidationError) as err:
        validate_schema(schema)
    assert validation_error_msg in err.value.message


GOOD_SCHEMAS = ["array.yaml", "nested-array.yaml", "basic.yaml"]


@pytest.mark.parametrize("schema_file", GOOD_SCHEMAS)
def test_good_validations(schema_file):
    """
    Validation fails because the schema is missing
    a redactionPolicies field.
    """
    # Read the schema file
    with open(SCHEMA_PATH / "good" / schema_file) as f:
        schema = yaml.loads(f)
    # Assert that the schema files for a known reason.
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
