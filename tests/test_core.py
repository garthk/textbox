import importlib

from packaging.version import parse


def test_core_package() -> None:
    core = importlib.import_module("textbox.core")
    version = core.__version__
    assert isinstance(version, str)
    assert parse(version)
