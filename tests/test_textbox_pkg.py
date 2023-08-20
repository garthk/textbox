import importlib

from packaging.version import parse


def test_core_package() -> None:
    textbox = importlib.import_module("textbox")
    version = textbox.__version__
    assert isinstance(version, str)
    assert parse(version)
