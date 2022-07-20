# mypy: ignore-errors

# try:
#     from ruamel.yaml import YAML
# except ImportError as e:
#     # check for known conda bug that prevents
#     # pip from installing ruamel.yaml dependency
#     try:
#         import ruamel_yaml  # noqa
#     except ImportError:
#         # nope, regular import error; raise original
#         raise e
#     else:
#         # have conda fork ruamel_yaml, but not ruamel.yaml.
#         # this is a bug in the ruamel_yaml conda package
#         # mistakenly identifying itself as ruamel.yaml to pip.
#         # conda install the 'real' ruamel.yaml to fix
#         raise ImportError(
#             "Missing dependency ruamel.yaml. Try: `conda install ruamel.yaml`"
#         )
import pathlib

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
    data = pathlib.Path(str(fpath)).read_text()
    return loads(data)


def dump(data, outpath):
    pathlib.Path(outpath).write_text(dumps(data))
