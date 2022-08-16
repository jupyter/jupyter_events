"""A module with pre-defined, configurable Redactor objects
that are useful for handling redacted data in a Jupyter
Events logger.
"""
import re

from traitlets import Dict, List, TraitType, Unicode, default
from traitlets.config import Configurable


class RedactedProperties(TraitType):
    """A trait type for validating the `redacted_properties`
    trait in Redactor objects.
    """

    info_text = (
        "a list of properties to redact. This should be a list "
        "of tuples with the form "
        "(schema_id: str, version: int, property_name: str) "
    )

    def validate(self, obj, value):
        try:
            assert type(value) == list

            for prop in value:
                assert type(prop) == tuple
                assert type(prop[0]) == str
                assert type(prop[1]) == int
                assert type(prop[2]) == str
            return value
        except AssertionError:
            self.error(obj, value)


class RedactedSchemas(TraitType):
    """A trait type for validating the `redacted_properties`
    trait in Redactor objects.
    """

    info_text = (
        "a list of schemas to redact. This should be a list "
        "of tuples with the form "
        "(schema_id: str, version: int) "
    )

    def validate(self, obj, value):
        try:
            assert type(value) == list

            for prop in value:
                assert type(prop) == tuple
                assert type(prop[0]) == str
                assert type(prop[1]) == int
            return value
        except AssertionError:
            self.error(obj, value)


class BaseRedactor(Configurable):
    """The base class for redactor objects that mutate
    data in a Jupyter Events `EventLogger` object.
    """

    redacted_properties = RedactedProperties([]).tag(config=True)
    redacted_patterns = List().tag(config=True)
    redacted_schemas = RedactedSchemas([]).tag(config=True)

    _mapping_redacted_properties = Dict()

    @default("_mapping_redacted_properties")
    def _default_mapping_redacted_properties(self):
        """Building a mapping to properties for more efficient look-up."""
        mapping_properties = {}
        for (schema_id, version, key) in self.redacted_properties:
            try:
                mapping_properties[(schema_id, version)].append(key)
            except KeyError:
                mapping_properties[(schema_id, version)] = [key]
        return mapping_properties

    _regex_redacted_patterns = List()

    @default("_regex_redacted_patterns")
    def _default_regex_redacted_patterns(self):
        return [re.compile(pat) for pat in self.redacted_patterns]

    def _action(self, data: dict, key: str):
        pass

    def __call__(self, schema_id: str, version: int, data: dict) -> dict:
        # If found in the redacted schemas, remove all data.
        if (schema_id, version) in self.redacted_schemas:
            for key in data:
                self._action(data, key)
            return data

        # Build a list of keys to redact. We will iterate over
        # these keys later, to avoid changing to dictionary size while iterating.
        keys_to_redact = []
        for key in data:
            # First, check if this property is special cased in the redacted_properties
            try:
                if key in self._mapping_redacted_properties[(schema_id, version)]:
                    keys_to_redact.append(key)
            # If not, check if the property matches any redacted property patterns
            except KeyError:
                for pat in self._regex_redacted_patterns:
                    # Compute a full match check:
                    if pat.fullmatch(key):
                        keys_to_redact.append(key)

        for key in keys_to_redact:
            self._action(data, key)
        return data


class RemovalRedactor(BaseRedactor):
    """A redactor that deletes redacted data from an incoming event before it is emitted."""

    def _action(self, data: dict, key: str):
        data.pop(key)


class MaskRedactor(BaseRedactor):
    """A redactor that replaces redacted data in an incoming event with masking string."""

    mask_string = Unicode("<masked>").tag(config=True)

    def _action(self, data: dict, key: str):
        data[key] = self.mask_string
