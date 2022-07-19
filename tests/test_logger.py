import logging

import pytest
from traitlets import TraitError
from traitlets.config.loader import PyFileConfigLoader

from jupyter_events.logger import EventLogger

GOOD_CONFIG = """
import logging

c.EventLogger.handlers = [
    logging.StreamHandler()
]
"""

BAD_CONFIG = """
import logging

c.EventLogger.handlers = [
    0
]
"""


def get_config_from_file(path, content):
    # Write config file
    filename = "config.py"
    config_file = path / filename
    config_file.write_text(content)

    # Load written file.
    loader = PyFileConfigLoader(filename, path=str(path))
    cfg = loader.load_config()
    return cfg


def test_good_config_file(tmp_path):
    cfg = get_config_from_file(tmp_path, GOOD_CONFIG)

    # Pass config to EventLogger
    e = EventLogger(config=cfg)

    assert len(e.handlers) > 0
    assert isinstance(e.handlers[0], logging.Handler)


def test_bad_config_file(tmp_path):
    cfg = get_config_from_file(tmp_path, BAD_CONFIG)

    with pytest.raises(TraitError):
        EventLogger(config=cfg)
