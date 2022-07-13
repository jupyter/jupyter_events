from multiprocessing import Event

from .schema import EventSchema


class SchemaRegistryException(Exception):
    pass


class SchemaRegistry:
    def __init__(self, schemas={}, allowed_policies="all"):
        self._schemas = schemas
        self._allowed_policies = allowed_policies

    @property
    def allowed_policies(self):
        return self._allowed_policies

    def __contains__(self, registry_key):
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

    def register(self, schema_data):
        """Register a schema."""
        schema = EventSchema(schema_data, allowed_policies=self.allowed_policies)
        self._add(schema)

    def register_from_file(self, schema_filepath):
        """Register a schema from a file."""
        schema = EventSchema.from_file(
            schema_filepath, allowed_policies=self.allowed_policies
        )
        self._add(schema)

    def get(self, registry_key) -> EventSchema:
        try:
            return self._schemas[registry_key]
        except KeyError:
            raise KeyError(
                f"The requested schema, {registry_key[0]} "
                f"(version {registry_key[1]}), was not found in the "
                "schema registry. Are you sure it was previously registered?"
            )

    def remove(self, registry_key):
        try:
            del self._schemas[registry_key]
        except KeyError:
            raise KeyError(
                f"The requested schema, {registry_key[0]} "
                f"(version {registry_key[1]}), was not found in the "
                "schema registry. Are you sure it was previously registered?"
            )
