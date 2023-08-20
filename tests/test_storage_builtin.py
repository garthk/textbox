import os
import pathlib as p
import typing as t

import textbox.storage.builtin
from textbox import BoxOpener, OpenTheBox, Text
from textbox.storage.builtin import (
    BuiltinBox,
    _data_dir,
    _insertion_sql,
    _shorten_sql,
    open_the_box,
)


def test_builtin_protocols() -> None:
    assert isinstance(textbox.storage.builtin, BoxOpener)
    assert isinstance(textbox.storage.builtin.open_the_box, OpenTheBox)


def test_builtin_box_opener() -> None:
    environ = {"TEXTBOX_LOCATION": ":memory:"}
    box = open_the_box(environ=environ)
    assert isinstance(box, BuiltinBox)
    # TODO ensure appropriate non-null values:
    text = Text(
        captured=None,
        created=None,
        modified=None,
        url=None,
        content=None,
        content_type=None,
        metadata=None,
    )
    box.put([text])
    box.close()


def test__data_dir() -> None:
    d = _data_dir("app", os.environ)
    assert isinstance(d, p.Path)

    d = _data_dir("app", {})
    assert isinstance(d, p.Path)


def test__shorten_sql() -> None:
    sql = """
        some SQL in
        a heredoc
        """
    result = _shorten_sql(sql)
    assert result == "some SQL in a heredoc"


def test__insertion_sql() -> None:
    class Noun(t.Protocol):
        i: int
        s: str

    shorter_sql = _insertion_sql("noun", Noun)
    assert shorter_sql == "INSERT OR REPLACE INTO [noun] ([i], [s]) VALUES (:i, :s);"

    longer_sql = _insertion_sql("text", Text)
    expected_shape = ["INSERT...", "[table] (...)", "VALUES", "(...);"]
    assert len(longer_sql.split("\n")) == len(expected_shape)
