"Command line."

import importlib.metadata
import sys

__all__ = ["__version__", "main"]

__version__ = importlib.metadata.version("textbox")


def main() -> None:
    "Command line entry point."
    sys.exit(0)
