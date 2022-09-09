import jupyter_events
from jupyter_events.cli import RC

from .utils import SCHEMA_PATH

NAME = "jupyter-events"
VALIDATE = NAME, "validate"


def test_cli_version(script_runner):
    ret = script_runner.run(NAME, "--version")
    assert ret.success
    assert ret.stdout.strip() == f"{NAME}, version {jupyter_events.__version__}"


def test_cli_help(script_runner):
    ret = script_runner.run(NAME, "--help")
    assert ret.success
    assert f"Usage: {NAME}" in ret.stdout.strip()


def test_cli_good(script_runner):
    """jupyter events validate path/to/my_schema.json"""
    ret = script_runner.run(*VALIDATE, SCHEMA_PATH / "good/array.yaml")
    assert ret.success
    assert not ret.stderr.strip()
    assert "This schema is valid" in ret.stdout


def test_cli_missing(script_runner):
    ret = script_runner.run(*VALIDATE, SCHEMA_PATH / "bad/doesnt-exist.yaml")
    assert not ret.success
    assert ret.returncode == RC.UNPARSEABLE
    assert "Schema file not present" in ret.stderr.strip()


def test_cli_malformed(script_runner):
    ret = script_runner.run(*VALIDATE, SCHEMA_PATH / "bad/invalid.yaml")
    assert not ret.success
    assert ret.returncode == RC.UNPARSEABLE
    assert "Could not deserialize" in ret.stderr.strip()


def test_cli_invalid(script_runner):
    ret = script_runner.run(*VALIDATE, SCHEMA_PATH / "bad/reserved-property.yaml")
    assert not ret.success
    assert ret.returncode == RC.INVALID
    assert "The schema failed to validate" in ret.stderr.strip()
