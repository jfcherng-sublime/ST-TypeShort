from typing import Any, Dict, List

from .types import CompiledBinding


class G:
    """This class stores application-level "G"lobal variables."""

    syntax_infos: Dict[str, Any] = {
        # syntax_file: {
        #     "file_basename": file_basename,
        #     "file_ext": file_ext,  # with dot
        #     "file_name": file_name,  # no ext
        #     "file_path": syntax_file,
        #     "syntax_name": syntax_name,
        #     "syntax_ids": syntax_ids,  # names represent this syntax
        # },
        # ...
    }

    bindings: List[CompiledBinding] = []
    """Compiled from user settings `bindings` via `BindingsCompiler`."""
