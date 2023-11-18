from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict


class BindingDict(TypedDict):
    syntax_list: list[str]
    keymaps: dict[str, str]


@dataclass
class CompiledBinding:
    syntax_list: set[str]
    syntax_list_selector: str
    keymaps: dict[str, str]
    keymaps_search_max_length: int


@dataclass
class ReplacementJob:
    region: tuple[int, int]
    replacement: str


class ReplacementJobDict(TypedDict):
    region: list[int]
    replacement: str
