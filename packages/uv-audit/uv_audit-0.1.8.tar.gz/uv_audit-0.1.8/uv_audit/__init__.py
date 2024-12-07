from importlib import metadata as _metadata

from uv_audit.cli import cli  # noqa: F401

try:
    __version__ = _metadata.version('uv-audit')

except _metadata.PackageNotFoundError:
    __version__ = '0.0.0'
