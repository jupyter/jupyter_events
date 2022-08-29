import json
import pathlib

import click
from jsonschema import ValidationError
from rich.console import Console
from rich.json import JSON
from rich.markup import escape
from rich.padding import Padding
from rich.style import Style

from jupyter_events.schema import EventSchema, EventSchemaLoadingError

console = Console()


@click.group()
def main():
    """A simple CLI tool to quickly validate JSON schemas against
    Jupyter Event's custom validator.

    You can see Jupyter Event's meta-schema here:

        https://raw.githubusercontent.com/jupyter/jupyter_events/main/jupyter_events/schemas/event-metaschema.yml
    """
    pass


@click.command()
@click.argument("schema")
def validate(schema):
    """Validate a SCHEMA against Jupyter Event's meta schema.

    SCHEMA can be a JSON/YAML string or filepath to a schema.
    """
    console.rule("Validating the following schema", style=Style(color="blue"))
    # Soft load the schema without validating.
    try:
        _schema = EventSchema._load_schema(schema)
    except EventSchemaLoadingError:
        schema_path = pathlib.Path(schema)
        _schema = EventSchema._load_schema(schema_path)
    # Print what was found.
    schema_json = JSON(json.dumps(_schema))
    console.print(Padding(schema_json, (1, 0, 1, 4)))
    # Now validate this schema against the meta-schema.
    try:
        EventSchema(_schema)
        console.rule("Results", style=Style(color="green"))
        out = Padding(
            "[green]\u2714[white] Nice work! This schema is valid.", (1, 0, 1, 0)
        )
        console.print(out)
    except ValidationError as err:
        console.rule("Results", style=Style(color="red"))
        console.print("[red]\u274c [white]The schema failed to validate.\n")
        console.print("We found the following error with your schema:")
        out = escape(str(err))
        console.print(Padding(out, (1, 0, 1, 4)))


main.add_command(validate)
