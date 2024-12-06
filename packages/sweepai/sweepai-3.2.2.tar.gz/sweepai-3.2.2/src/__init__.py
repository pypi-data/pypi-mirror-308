from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version(__package__) # type: ignore
except PackageNotFoundError:
    __version__ = "0.0.0"