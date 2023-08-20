"Remember text for you, wholesale."

import dataclasses
import datetime
import importlib.metadata
import typing as t

__all__ = ["__version__"]

__version__ = importlib.metadata.version("textbox")


@dataclasses.dataclass
class Text:
    "Text on its way to or from the box."

    captured: datetime.datetime
    created: datetime.datetime | None
    modified: datetime.datetime | None
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
class OpenTheBox(t.Protocol):
    "Functions satisfying this protocol might open boxes."

    def __call__(self) -> Box:
        "Open the box."
        ...


@t.runtime_checkable
class BoxOpener(t.Protocol):
    "Modules satisfying this protocol implement our storage API."

    open_the_box: OpenTheBox
