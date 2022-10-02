from typing import Any, Dict, List

from .compiler import BindingType


class G:
    """This class stores application-level "G"lobal variables."""

    syntax_infos = {
        # syntax_file: {
        #     "file_basename": file_basename,
        #     "file_ext": file_ext,  # with dot
        #     "file_name": file_name,  # no ext
        #     "file_path": syntax_file,
        #     "syntax_name": syntax_name,
        #     "syntax_ids": syntax_ids,  # names represent this syntax
        # },
        # ...
    }  # type: Dict[str, Any]

    bindings = []  # type: List[BindingType]
    """Compiled from user settings `bindings` via `BindingsCompiler`."""
