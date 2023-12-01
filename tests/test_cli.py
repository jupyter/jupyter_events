from __future__ import annotations

import os

import pytest

import jupyter_events
from jupyter_events.cli import RC

from .utils import SCHEMA_PATH

NAME = "jupyter-events"
VALIDATE = NAME, "validate"


@pytest.fixture
def cli(script_runner):
    def run_cli(*args, **kwargs):
        env = dict(os.environ)
        env.update(kwargs.pop("env", {}))
        env["PYTHONIOENCODING"] = "utf-8"
        kwargs["env"] = env
        return script_runner.run([NAME, *list(map(str, args))], **kwargs)

    return run_cli


def test_cli_version(cli):
    ret = cli("--version")
    assert ret.success
    assert ret.stdout.strip() == f"{NAME}, version {jupyter_events.__version__}"


def test_cli_help(cli):
    ret = cli("--help")
    assert ret.success
    assert f"Usage: {NAME}" in ret.stdout.strip()


def test_cli_good(cli):
    """jupyter events validate path/to/my_schema.json"""
    ret = cli("validate", SCHEMA_PATH / "good/array.yaml")
    assert ret.success
    assert not ret.stderr.strip()
    assert "This schema is valid" in ret.stdout


def test_cli_good_raw(cli):
    """jupyter events validate path/to/my_schema.json"""
    ret = cli("validate", (SCHEMA_PATH / "good/array.yaml").read_text(encoding="utf-8"))
    assert ret.success
    assert not ret.stderr.strip()
    assert "This schema is valid" in ret.stdout


def test_cli_missing(cli):
    ret = cli("validate", SCHEMA_PATH / "bad/doesnt-exist.yaml")
    assert not ret.success
    assert ret.returncode == RC.UNPARSABLE
    assert "Schema file not present" in ret.stderr.strip()


def test_cli_malformed(cli):
    ret = cli("validate", SCHEMA_PATH / "bad/invalid.yaml")
    assert not ret.success
    assert ret.returncode == RC.UNPARSABLE
    assert "Could not deserialize" in ret.stderr.strip()


def test_cli_invalid(cli):
    ret = cli("validate", SCHEMA_PATH / "bad/reserved-property.yaml")
    assert not ret.success
    assert ret.returncode == RC.INVALID
    assert "The schema failed to validate" in ret.stderr.strip()
