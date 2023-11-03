from pathlib import Path

from todo_issues.models import TodoItem
from todo_issues.parse import parse_file


def test_parse_file():
    file = Path("example/example/main.py")

    expected = [
        TodoItem(
            scope=None,
            content="module docstring",
            file=file,
            token=None,
        ),
        TodoItem(
            scope="CI",
            content="comment",
            file=file,
            token=None,
        ),
        TodoItem(
            scope=None,
            content="multiline",
            file=file,
            token=None,
        ),
        TodoItem(
            scope=None,
            content="function docstring",
            file=file,
            token=None,
        ),
        TodoItem(
            scope=None,
            content="indented comment",
            file=file,
            token=None,
        ),
        TodoItem(
            scope=None,
            content="another comment",
            file=file,
            token=None,
        ),
        TodoItem(
            scope=None,
            content="yet another comment",
            file=file,
            token=None,
        ),
    ]

    for result, expect in zip(parse_file(file), expected, strict=True):
        assert (result.scope, result.content) == (expect.scope, expect.content)
