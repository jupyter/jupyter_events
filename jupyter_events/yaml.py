# mypy: ignore-errors
from pathlib import Path

from yaml import dump as ydump
from yaml import load as yload

try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader


def loads(stream):
    return yload(stream, Loader=Loader)


def dumps(stream):
    return ydump(stream, Dumper=Dumper)


def load(fpath):
    # coerce PurePath into Path, then read its contents
    data = Path(str(fpath)).read_text()
    return loads(data)


def dump(data, outpath):
    Path(outpath).write_text(dumps(data))
