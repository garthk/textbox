"Remember text for you, wholesale."

import importlib.metadata
import typing as t

__all__ = ["__version__"]

__version__ = importlib.metadata.version("textbox")


@t.runtime_checkable
class Text(t.Protocol):
    "Text on its way to or from the box."

    captured: str
    created: str | None
    modified: str | None
    url: str
    content: str
    content_type: str | None
    metadata: str | None


class Box(t.Protocol):
    "The box into which we put the text."

    def put(self, texts: t.Iterable[Text]) -> None:
        "Put text into the box. Middling idempotent."
        ...

    def close(self) -> None:
        "Close the box."
        ...


@t.runtime_checkable
class BoxOpener(t.Protocol):
    "Modules satisfying this protocol implement our storage API."

    def open(self) -> Box:  # noqa: A003
        "Open the box."
        ...
