import importlib
import types

from packaging.version import parse


def test_cli_package() -> None:
    cli = importlib.import_module("textbox.cli")
    assert hasattr(cli, "__version__")
    assert hasattr(cli, "main")

    assert isinstance(cli.main, types.FunctionType)
    version = cli.__version__
    assert isinstance(version, str)
    assert parse(version)
