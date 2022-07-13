import pathlib
from typing import Any, Dict, Hashable, List, Sequence, Union

from jsonschema import RefResolver, validators

from .yaml import yaml


def _nested_pop(dictionary: dict, nested_keys: Sequence[Hashable]) -> Any:
    """Pop a item nested anywhere in a dwictionary using the
    list of (hashable) keys to locate the item.
    """
    d = dictionary
    last_entry = nested_keys[-1]
    for key in nested_keys[:-1]:
        d = d[key]
    return d.pop(last_entry)


def _get_redaction_policies(schema: dict):
    """A recursive function that iterates an event schema
    and returns a mapping of redaction policies to
    (nested) properties (identified by a sequence of keys).
    """
    redaction_policies: Dict[str, List[str]] = {}

    def _extract_policies(subschema, key_sequence=()):
        props = subschema["properties"]
        for key, obj in props.items():
            updated_key_sequence = key_sequence + (key,)
            if isinstance(obj, dict) and "properties" in obj:
                _extract_policies(obj, updated_key_sequence)

            # Update the list in place.
            for policy in obj["redactionPolicy"]:
                policies_list = redaction_policies.get(policy, [])
                policies_list.append(updated_key_sequence)
                redaction_policies[policy] = policies_list

    # Start the recursion
    _extract_policies(schema)
    return redaction_policies


METASCHEMA_PATH = pathlib.Path(__file__).parent.joinpath("schemas")
EVENT_METASCHEMA_FILEPATH = METASCHEMA_PATH.joinpath("event-metaschema.yml")
EVENT_METASCHEMA = yaml.load(EVENT_METASCHEMA_FILEPATH)
PROPERTY_METASCHEMA_FILEPATH = METASCHEMA_PATH.joinpath("property-metaschema.yml")
PROPERTY_METASCHEMA = yaml.load(PROPERTY_METASCHEMA_FILEPATH)
METASCHEMA_RESOLVER = RefResolver(
    base_uri=EVENT_METASCHEMA["$id"],
    referrer=EVENT_METASCHEMA,
    store={PROPERTY_METASCHEMA["$id"]: PROPERTY_METASCHEMA},
)
METASCHEMA_VALIDATOR = validators.Draft7Validator(
    EVENT_METASCHEMA, resolver=METASCHEMA_RESOLVER
)


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
        allowed_policies: Union[str, list] = "all",
    ):
        # Validate the schema against Jupyter Events metaschema.
        METASCHEMA_VALIDATOR.validate(schema)
        # Build a mapping of all property redaction policies.
        self._redaction_policies = _get_redaction_policies(schema)
        self._allowed_policies = self._validate_allowed_policies(allowed_policies)
        # Create a validator for this schema
        self._validator = validator_class(schema, resolver=resolver)
        self._schema = schema

    def _validate_allowed_policies(self, allowed_policies):
        value_type = type(allowed_policies)
        if value_type == str and allowed_policies == "all":
            return set(self.redaction_policies.keys())
        elif value_type == list:
            return set(["unrestricted"] + list(allowed_policies))
        raise TypeError(
            "allowed_policies must be the literal string, 'all', or a list of "
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
    def allowed_policies(self):
        """The redaction policies that will not be redacted when an
        incoming event is processed.
        """
        return self._allowed_policies

    @classmethod
    def from_file(
        cls,
        filepath,
        validator_class=validators.Draft7Validator,
        resolver=None,
        allowed_policies="all",
    ):
        schema = yaml.load(filepath)
        return cls(
            schema=schema,
            validator_class=validator_class,
            resolver=resolver,
            allowed_policies=allowed_policies,
        )

    @property
    def redaction_policies(self) -> Dict[str, List[str]]:
        """Mapping of the redaction policies in this schema to
        the (nested) properties where they are defined.
        """
        return self._redaction_policies

    def validate(self, data: dict) -> None:
        """Validate an incoming instance of this event schema."""
        self._validator.validate(data)

    def enforce_redaction_policy(self, data: dict) -> None:
        """Redact fields from"""
        # Find all policies not explicitly allowed.
        named_policies = set(self.redaction_policies.keys())
        redacted_policies = named_policies - self.allowed_policies
        for policy in redacted_policies:
            for property in self.redaction_policies[policy]:
                _nested_pop(data, property)

    def process(self, data: dict) -> None:
        """Validate event data and enforce an redaction policies."""
        self.validate(data)
        self.enforce_redaction_policy(data)
