import importlib
import typing as t


def test_cli_package() -> None:
    cli = importlib.import_module("textbox.cli")
    assert hasattr(cli, "main")
    assert isinstance(cli.main, t.Callable)
