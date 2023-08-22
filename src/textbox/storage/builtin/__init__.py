"""
Builtin storage provider, or "BoxOpener".

I'm trying to keep the core dependency tree small in count, depth, and complexity.
This is around 0.1 KLOC using just the included batteries.
SQLAlchemy is 200.0 KLOC.
"""

import importlib.metadata

__all__ = ["__version__"]

__version__ = importlib.metadata.version("textbox")

import collections
import functools
import importlib.resources
import logging
import os
import pathlib as p
import re
import sqlite3
import sys
import textwrap
import typing as t

from textbox import Box, BoxOpener, OpenTheBox, Text

_Environ: t.TypeAlias = t.Mapping[str, str]
_Pathish: t.TypeAlias = str | bytes | p.Path

__all__ = ["DEFAULT_FILENAME", "Box", "BoxOpener"]
logger = logging.getLogger(__name__)
DEFAULT_FILENAME = "textbox.db"  #: The default database filename
SCHEMATA_FILENAME = "textbox.sql"
TEXTBOX_IN_MEMORY = ":memory:"


def open_the_box(
    *,
    environ: _Environ | None,  #: override the environment for testing
) -> Box:
    "Open the built-in box."
    location: str | p.Path
    match environ := environ or os.environ:
        case {"TEXTBOX_LOCATION": ":memory:"}:
            location = ":memory:"
        case {"TEXTBOX_LOCATION": l}:
            location = l
        case _:
            location = _data_dir("textbox", environ) / DEFAULT_FILENAME

    if isinstance(location, p.Path):
        location.mkdir(exist_ok=True, parents=True)

    con = _connect(location)
    _create_tables(con)
    return BuiltinBox(con)


class BuiltinBox(Box):
    "The box into which we put the text."

    con: sqlite3.Connection | None
    put_sql: str

    def __init__(self, con: sqlite3.Connection) -> None:
        "Initialise the box."
        self.con = con
        self.put_sql = _insertion_sql("text", Text)

    def put(self, texts: t.Iterable[Text]) -> None:
        "Put text into the box. Middling idempotent."
        assert self.con  # noqa: S101
        with self.con as tx:
            tx.executemany(
                self.put_sql,
                (collections.defaultdict(None, text.__dict__) for text in texts),
            )

    def close(self) -> None:
        "Close the box."
        if not self.con:
            return
        self.con.close()
        self.con = None


assert isinstance(open_the_box, OpenTheBox)  # noqa: S101
assert isinstance(sys.modules[__name__], BoxOpener)  # noqa: S101

if t.TYPE_CHECKING:
    _otb: OpenTheBox = open_the_box  # satisfies function plugin protocol :noindex:
    _bo: BoxOpener = sys.modules[__name__]  # satisfies module plugin protocol :noindex:


def _connect(database: _Pathish) -> sqlite3.Connection:
    "Connect to our database at a particular path."
    logger.debug("connecting to %s...", database)
    con = sqlite3.Connection(database)
    con.row_factory = sqlite3.Row
    return con


def _create_tables(con: sqlite3.Connection) -> None:
    "Create our tables."
    files = importlib.resources.files(__name__)
    schemata = files.joinpath(SCHEMATA_FILENAME).read_text().split("\n\n")
    with con:
        for schema in schemata:
            logger.debug("%s", schema)
            con.execute(schema)


def _insertion_sql(table: str, prototype: type[Text]) -> str:
    "Generate an insertion statement."
    fields = prototype.__annotations__.keys()
    columns = ", ".join(f"[{f}]" for f in fields)
    values = ", ".join(f":{f}" for f in fields)
    return _shorten_sql(
        f"""
        INSERT OR REPLACE INTO
            [{table}] ({columns})
        VALUES
            ({values});
        """,
    )


def _shorten_sql(sql: str, *, width: int = 76) -> str:
    "Shorten SQL, as it'll likely end up in our telemetry."
    _sql = textwrap.dedent(sql).strip()
    line = re.sub(r"\s+", " ", textwrap.fill(_sql, width=width))
    return line if len(line) < width else _sql


# I'd prefer to use decorators, but MyPy.
_insertion_sql = functools.cache(_insertion_sql)
_shorten_sql = functools.cache(_shorten_sql)


def _data_dir(app: str, environ: _Environ = os.environ) -> p.Path:
    """
    Figure out where to put the user's data.

    Un-necessarily complicated unless you have Strong Opinions.
    Insufficiently thorough if you have Strong Opinions.
    """
    if data := environ.get("XDG_DATA_HOME", None):
        return p.Path(data) / app
    match sys.platform:
        case "darwin":
            return p.PosixPath("~/Library/Application Support").expanduser() / app
        case "win32":
            return p.WindowsPath(environ["LOCALAPPDATA"]) / app / "Data"
        case _:
            return p.PosixPath("~/.local/share").expanduser() / app
