class Globals(object):
    """
    @brief This class stores application-level global variables.
    """

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
    }

    # compiled from user settings "bindings" via "BindingsCompiler"
    # see "BindingsCompiler.py" for values
    bindings = []
