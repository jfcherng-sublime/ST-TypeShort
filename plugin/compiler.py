from __future__ import annotations

from typing import Generator

from .types import BindingDict, CompiledBinding


class BindingsCompiler:
    _required_keys = {"syntax_list", "keymaps"}

    def __init__(self, bindings: list[BindingDict] | None = None) -> None:
        self._bindings = bindings or []

    def compile(self) -> Generator[CompiledBinding, None, None]:
        yield from (binding for binding in map(self._compile_binding, self._bindings) if binding)

    def _compile_binding(self, binding: BindingDict) -> CompiledBinding | None:
        if not all((key in binding) for key in self._required_keys):
            return None

        return CompiledBinding(
            syntax_list=set(binding["syntax_list"]),
            syntax_list_selector="|".join(binding["syntax_list"]),
            keymaps=dict(binding["keymaps"]),
            keymaps_search_max_length=max(map(len, binding["keymaps"].keys())),
        )
