from dataclasses import dataclass
from pathlib import Path
from tokenize import TokenInfo
from typing import Optional


@dataclass(frozen=True)
class TodoItem:
    scope: Optional[str]
    content: str
    file: Path
    token: TokenInfo
