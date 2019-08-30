import copy
from typing import Dict, List


class BindingsCompiler(object):
    bindings = []
    binding_required_keys = ["syntax_list", "keymaps"]

    def __init__(self, bindings: List[Dict] = []) -> None:
        self.bindings = copy.deepcopy(bindings)

    def compile(self) -> List:
        return [binding for binding in map(self._compile_binding, self.bindings) if binding]

    def _compile_binding(self, binding: Dict) -> Dict:
        if not all(key in binding for key in self.binding_required_keys):
            return None

        binding_c = {}

        binding_c["syntax_list"] = set(binding["syntax_list"])
        binding_c["syntax_list_selector"] = "|".join(binding_c["syntax_list"])
        binding_c["keymaps"] = dict(binding["keymaps"])  # copy
        binding_c["keymaps_search_max_length"] = max(map(len, binding["keymaps"].keys()))

        return binding_c
