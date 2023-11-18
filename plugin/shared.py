from __future__ import annotations

from .types import CompiledBinding


class G:
    """This class stores application-level "G"lobal variables."""

    bindings: list[CompiledBinding] = []
    """Compiled from user settings `bindings` via `BindingsCompiler`."""
