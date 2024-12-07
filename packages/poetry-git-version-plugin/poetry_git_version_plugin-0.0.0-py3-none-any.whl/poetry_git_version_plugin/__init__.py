from importlib import metadata as _metadata

try:
    __version__ = _metadata.version('poetry-git-version-plugin')

except _metadata.PackageNotFoundError:  # pragma: no cover
    __version__ = '0.0.0'
