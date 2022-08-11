import json

import click
from jsonschema import ValidationError
from rich.console import Console
from rich.json import JSON
from rich.markup import escape
from rich.padding import Padding

from jupyter_events.schema import EventSchema

console = Console()


@click.group()
def main():
    pass


@click.command()
@click.argument("schema")
def validate(schema):
    """Validate a SCHEMA against Jupyter Event's meta schema.

    SCHEMA can be a JSON/YAML string or filepath to a schema.
    """
    console.rule("Validating the following schema")
    # Soft load the schema without validating.
    _schema = EventSchema._load_schema(schema)
    # Print what was found.
    schema_json = JSON(json.dumps(_schema))
    console.print(Padding(schema_json, (1, 0, 1, 4)))
    # Now validate this schema against the meta-schema.
    console.rule("Results")
    try:
        EventSchema(_schema)
        out = Padding(
            "[green]\u2714[white] Nice work! This schema is valid.", (1, 0, 1, 0)
        )
        console.print(out)
    except ValidationError as err:
        console.print("[red]\u274c [white]The schema failed to validate.\n")
        console.print("We found the following error with your schema:")
        out = escape(str(err))
        console.print(Padding(out, (1, 0, 1, 4)))


main.add_command(validate)
