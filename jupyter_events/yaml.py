# mypy: ignore-errors
from pathlib import Path

from yaml import dump as ydump
from yaml import load as yload

try:
    from yaml import CSafeDumper as SafeDumper
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeDumper, SafeLoader


def loads(stream):
    return yload(stream, Loader=SafeLoader)


def dumps(stream):
    return ydump(stream, Dumper=SafeDumper)


def load(fpath):
    # coerce PurePath into Path, then read its contents
    data = Path(str(fpath)).read_text()
    return loads(data)


def dump(data, outpath):
    Path(outpath).write_text(dumps(data))
