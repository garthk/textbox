"Remember text for you, wholesale."

import abc
import dataclasses
import datetime
import importlib
import importlib.metadata
import typing as t

from textbox.plugins import MF, PluginMap, find_plugins

__all__ = ["__version__"]

__version__ = importlib.metadata.version("textbox")


@dataclasses.dataclass
class Text:
    """
    Text on its way to or from the box.

    captured, uri, and content MUST be populated.
    content_type SHOULD be populated.
    """

    # fmt: off
    captured: datetime.datetime  #: When was this text captured?
    uri: str                     #: URI (includes URL, URN) identifying the text
    content: str                 #: The text itself
    metadata: str | None         #: JSON blob with any metadata for the text
    # fmt: on


class Generic(t.Protocol):
    ...


class Box(t.Protocol):
    "The box into which we put the text."

    @abc.abstractmethod
    def put(self, texts: t.Iterable[Text]) -> None:
        "Put text into the box. Middling idempotent."
        ...

    @abc.abstractmethod
    def close(self) -> None:
        "Close the box."
        ...


@t.runtime_checkable
class OpenTheBox(t.Protocol):
    "Functions satisfying this protocol might open boxes."

    def __call__(self) -> Box:
        "Open the box."
        ...


def plugged_storage() -> PluginMap[OpenTheBox]:
    "Find plugins implementing this protocol, either directly or via :py:class:`BoxOpener`."
    return find_plugins(
        namespace="textbox.storage",
        group="textbox.storage",
        adapter=_storage_adapter,
    )


@t.runtime_checkable
class BoxOpener(t.Protocol):
    "Modules satisfying this protocol implement our storage API."

    @abc.abstractmethod
    def open_the_box(self) -> Box:
        "Open the box."
        ...


def _storage_adapter(plugin: MF) -> OpenTheBox | None:
    if isinstance(plugin, BoxOpener):
        return _storage_adapter(plugin.open_the_box)
    if isinstance(plugin, OpenTheBox):
        return plugin
    return None


assert isinstance(BoxOpener.open_the_box, OpenTheBox)  # noqa: S101

if t.TYPE_CHECKING:
    _: OpenTheBox = BoxOpener.open_the_box
