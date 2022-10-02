from dataclasses import dataclass
from typing import Dict, List, Set, Tuple, TypedDict


class BindingDict(TypedDict):
    syntax_list: List[str]
    keymaps: Dict[str, str]


@dataclass
class CompiledBinding:
    syntax_list: Set[str]
    syntax_list_selector: str
    keymaps: Dict[str, str]
    keymaps_search_max_length: int


@dataclass
class ReplacementJob:
    region: Tuple[int, int]
    replacement: str


class ReplacementJobDict(TypedDict):
    region: List[int]
    replacement: str
