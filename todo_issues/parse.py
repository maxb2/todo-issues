import re
from pathlib import Path
from tokenize import COMMENT, STRING, TokenInfo, tokenize
from typing import List, Optional

from .models import TodoItem

TODO_ITEM_REGEX = re.compile(
    r".*TODO(:?\((?P<scope>.*?)\)){0,1}:\s*(?P<content>[^\n]*)(?:\n*\s*(?:'''|\"\"\")){0,1}",
    re.M | re.DOTALL,
)

TODO_SWITCH_REGEX = re.compile(
    r"^\s*#\s+todo\-issues:\s+(on/off|on|off)(?:\s.*){0,1}$", re.M | re.DOTALL
)


def parse_todo(file: Path, token: TokenInfo) -> Optional[TodoItem]:
    if match := TODO_ITEM_REGEX.match(token.string):
        return TodoItem(
            match.groupdict()["scope"], match.groupdict()["content"], file, token
        )


def parse_todo_switch(todo_switch: bool, string: str) -> bool:
    if match := TODO_SWITCH_REGEX.match(string):
        switch = match.group(1)
        if switch == "on":
            return True
        if switch == "off":
            return False
        if switch == "on/off":
            return not todo_switch
    return todo_switch


def parse_file(file: Path) -> List[TodoItem]:
    with open(file, "rb") as fp:
        tokens = list(tokenize(fp.readline))

    todo_switch = True

    todos: List[TodoItem] = []
    for token in tokens:
        if token.type == COMMENT:
            todo_switch = parse_todo_switch(todo_switch, token.string)
        if todo_switch and token.type in [STRING, COMMENT]:
            if todo := parse_todo(file, token):
                todos.append(todo)

    return todos
