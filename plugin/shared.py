from typing import List

from .types import CompiledBinding


class G:
    """This class stores application-level "G"lobal variables."""

    bindings: List[CompiledBinding] = []
    """Compiled from user settings `bindings` via `BindingsCompiler`."""
