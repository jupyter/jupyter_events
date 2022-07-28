import pytest
from jsonschema.exceptions import ValidationError

from jupyter_events import yaml
from jupyter_events.validators import validate_schema

from .utils import SCHEMA_PATH

MISSING_REDACTION_POLICY = "'redactionPolicies' is a required property"

BAD_SCHEMAS = [
    [
        # Bad schema file.
        "missing-parent-policies.yaml",
        # The expected valdation error message.
        MISSING_REDACTION_POLICY,
    ],
    ["missing-policy-array.yaml", MISSING_REDACTION_POLICY],
    ["missing-policy-nested-array.yaml", MISSING_REDACTION_POLICY],
    ["reserved-property.yaml", "Properties starting with 'dunder'"],
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
