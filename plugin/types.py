from dataclasses import dataclass
from typing import Dict, List, Set, TypedDict


@dataclass
class CompiledBinding:
    syntax_list: Set[str]
    syntax_list_selector: str
    keymaps: Dict[str, str]
    keymaps_search_max_length: int


class BindingDict(TypedDict):
    syntax_list: List[str]
    keymaps: Dict[str, str]
