from typing import Any, List, Optional, Tuple

from .schema import EventSchema


class SchemaRegistryException(Exception):
    """Exception class for Jupyter Events Schema Registry Errors."""


class SchemaRegistry:
    """A convenient API for storing and searching a group of schemas."""

    def __init__(self, schemas: dict = None, redacted_policies: list = None):
        self._schemas = schemas or {}
        self._redacted_policies = redacted_policies

    @property
    def redacted_policies(self) -> Optional[List[Any]]:
        """A list of policies that will be redacted from
        all events validated against this registry.
        """
        return self._redacted_policies

    def __contains__(self, registry_key: Tuple[str, int]):
        """Syntax sugar to check if a schema is found in the registry"""
        return registry_key in self._schemas

    def _add(self, schema_obj: EventSchema):
        if schema_obj.registry_key in self._schemas:
            raise SchemaRegistryException(
                f"The schema, {schema_obj.id} "
                f"(version {schema_obj.version}), is already "
                "registered. Try removing it and registering it again."
            )
        self._schemas[schema_obj.registry_key] = schema_obj

    def register(self, data: dict):
        """Add a valid schema to the registry.

        All schemas are validated against the Jupyter Events meta-schema
        found here:
        """
        schema = EventSchema(data, redacted_policies=self.redacted_policies)
        self._add(schema)

    def register_from_file(self, schema_filepath: str):
        """Register a schema from a file."""
        schema = EventSchema.from_file(
            schema_filepath, redacted_policies=self.redacted_policies
        )
        self._add(schema)

    def get(self, id: str, version: int) -> EventSchema:
        """Fetch a given schema. If the schema is not found,
        this will raise a KeyError.
        """
        try:
            return self._schemas[(id, version)]
        except KeyError:
            raise KeyError(
                f"The requested schema, {id} "
                f"(version {version}), was not found in the "
                "schema registry. Are you sure it was previously registered?"
            )

    def remove(self, id: str, version: int) -> None:
        """Remove a given schema. If the schema is not found,
        this will raise a KeyError.
        """
        try:
            del self._schemas[(id, version)]
        except KeyError:
            raise KeyError(
                f"The requested schema, {id} "
                f"(version {version}), was not found in the "
                "schema registry. Are you sure it was previously registered?"
            )

    def validate_event(self, id: str, version: int, data: dict) -> None:
        """Validate an event against a schema within this
        registry.
        """
        schema = self.get(id, version)
        schema.validate(data)

    def process_event(self, id: str, version: int, data: dict) -> None:
        """Validate and event and enforce an redaction policies (in place).
        Nothing is returned by this method, because the data is redacted in place.
        """
        schema = self.get(id, version)
        schema.process(data)
