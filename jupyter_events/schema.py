from typing import Any, Dict, Hashable, List, Sequence, Union

from jsonschema import validators

from .validators import JUPYTER_EVENTS_VALIDATOR
from .yaml import yaml


def _pop_nested_redacted_fields(
    schema_data: dict, policy_location: Sequence[Hashable]
) -> Any:
    """Pop a item nested anywhere in a dwictionary using the
    list of (hashable) keys to locate the item.
    """
    # Begin walking the sequence of keys to the policy
    # location given.
    nested_data = schema_data
    for i, el in enumerate(policy_location[:-1]):
        # Handle arrays of objects.
        if el == "__array__":
            for j, _ in enumerate(nested_data):
                branch = policy_location[i + 1 :]
                _pop_nested_redacted_fields(nested_data[j], branch)
            return
        # Try moving into nested child schema.
        try:
            nested_data = nested_data[el]
        except KeyError:
            return
    # If we made it this far, we ended on a policy that needs to be popped.
    return nested_data.pop(policy_location[-1])


def _find_redaction_policies(schema: dict):
    """A recursive function that iterates an event schema
    and returns a mapping of redaction policies to
    (nested) properties (identified by a sequence of keys).
    """
    redaction_policies: Dict[str, List[str]] = {}

    def _extract_policies(subschema, key_sequence=()):
        props = subschema["properties"]
        for key, obj in props.items():
            updated_key_sequence = key_sequence + (key,)

            def _nested_extract_policies(obj, updated_key_sequence):
                if isinstance(obj, dict):
                    if "properties" in obj:
                        _extract_policies(obj, updated_key_sequence)
                    if "items" in obj and "properties" in obj["items"]:
                        _nested_extract_policies(
                            obj["items"], updated_key_sequence + ("__array__",)
                        )

            _nested_extract_policies(obj, updated_key_sequence)

            # Update the list in place.
            for policy in obj["redactionPolicies"]:
                policies_list = redaction_policies.get(policy, [])
                policies_list.append(updated_key_sequence)
                redaction_policies[policy] = policies_list

    # Start the recursion
    _extract_policies(schema)
    return redaction_policies


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

    allowed_policies: set
        A set of redaction policied allowed by this event schema.
        Each property in the schema must have a `redactionPolicy`
        annotation representing the level of sensitivity of the
        data collected by this event. In order for that data
        to be emitted of Jupyter Events, the matching redaction
        policy must be listed here.

    """

    def __init__(
        self,
        schema,
        validator_class=validators.Draft7Validator,
        resolver=None,
        redacted_policies: Union[str, list, None] = None,
    ):
        # Validate the schema against Jupyter Events metaschema.
        JUPYTER_EVENTS_VALIDATOR.validate(schema)
        # Build a mapping of all property redaction policies.
        self._redaction_policies_locations = _find_redaction_policies(schema)
        self._redacted_policies = self._validate_redacted_policies(redacted_policies)
        # Create a validator for this schema
        self._validator = validator_class(schema, resolver=resolver)
        self._schema = schema

    def _validate_redacted_policies(self, redacted_policies):
        if redacted_policies is None:
            return set()
        value_type = type(redacted_policies)
        if value_type == str and redacted_policies == "all":
            return set(self.redaction_policies_locations.keys())
        if value_type == list:
            return set(redacted_policies)
        raise TypeError(
            "redacted_policies must be the literal string, 'all', or a list of "
            "redaction polices"
        )

    @property
    def id(self):
        """Schema $id field."""
        return self._schema["$id"]

    @property
    def version(self):
        """Schema's version."""
        return self._schema["version"]

    @property
    def registry_key(self):
        return (self.id, self.version)

    @property
    def redacted_policies(self):
        """The redaction policies that will not be redacted when an
        incoming event is processed.
        """
        return self._redacted_policies

    @classmethod
    def from_file(
        cls,
        filepath,
        validator_class=validators.Draft7Validator,
        resolver=None,
        redacted_policies=None,
    ):
        schema = yaml.load(filepath)
        return cls(
            schema=schema,
            validator_class=validator_class,
            resolver=resolver,
            redacted_policies=redacted_policies,
        )

    @property
    def redaction_policies_locations(self) -> Dict[str, List[str]]:
        """Mapping of the redaction policies in this schema to
        the (nested) properties where they are defined.
        """
        return self._redaction_policies_locations

    def validate(self, data: dict) -> None:
        """Validate an incoming instance of this event schema."""
        self._validator.validate(data)

    def enforce_redaction_policies(self, data: dict) -> None:
        """Redact fields from"""
        # # Find all policies not explicitly allowed.
        # named_policies = set(self.redaction_policies_locations.keys())
        # redacted_policies = named_policies - self.unredacted_policies
        for policy_type in self.redacted_policies:
            policy_locations = self._redaction_policies_locations[policy_type]
            print(policy_type, policy_locations)
            for item in policy_locations:
                _pop_nested_redacted_fields(data, item)

    def process(self, data: dict) -> None:
        """Validate event data and enforce an redaction policies."""
        self.validate(data)
        self.enforce_redaction_policies(data)
