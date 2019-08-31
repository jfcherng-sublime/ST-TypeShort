# Stubs for sublime_plugin (Python 3.5)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

api_ready = ...  # type: bool
application_command_classes = ...  # type: Any
window_command_classes = ...  # type: Any
text_command_classes = ...  # type: Any
view_event_listener_classes = ...  # type: Any
view_event_listeners = ...  # type: Any
all_command_classes = ...  # type: Any
all_callbacks = ...  # type: Any
profile = ...  # type: Any

def unload_module(module): ...
def unload_plugin(modulename): ...
def reload_plugin(modulename): ...
def create_application_commands(): ...
def create_window_commands(window_id): ...
def create_text_commands(view_id): ...
def on_api_ready(): ...
def is_view_event_listener_applicable(cls, view): ...
def create_view_event_listeners(classes, view): ...
def check_view_event_listeners(view): ...
def attach_view(view): ...

check_all_view_event_listeners_scheduled = ...  # type: bool

def check_all_view_event_listeners(): ...
def detach_view(view): ...
def event_listeners_for_view(view): ...
def find_view_event_listener(view, cls): ...
def on_new(view_id): ...
def on_new_async(view_id): ...
def on_clone(view_id): ...
def on_clone_async(view_id): ...

class Summary:
    max = ...  # type: float
    sum = ...  # type: float
    count = ...  # type: int
    def __init__(self) -> None: ...
    def record(self, x): ...

def run_callback(event, callback, expr): ...
def run_view_listener_callback(view, name): ...
def run_async_view_listener_callback(view, name): ...
def on_load(view_id): ...
def on_load_async(view_id): ...
def on_pre_close(view_id): ...
def on_close(view_id): ...
def on_pre_save(view_id): ...
def on_pre_save_async(view_id): ...
def on_post_save(view_id): ...
def on_post_save_async(view_id): ...
def on_modified(view_id): ...
def on_modified_async(view_id): ...
def on_selection_modified(view_id): ...
def on_selection_modified_async(view_id): ...
def on_activated(view_id): ...
def on_activated_async(view_id): ...
def on_deactivated(view_id): ...
def on_deactivated_async(view_id): ...
def on_query_context(view_id, key, operator, operand, match_all): ...
def normalise_completion(c): ...
def on_query_completions(view_id, prefix, locations): ...
def on_hover(view_id, point, hover_zone): ...
def on_text_command(view_id, name, args): ...
def on_window_command(window_id, name, args): ...
def on_post_text_command(view_id, name, args): ...
def on_post_window_command(window_id, name, args): ...

class Command:
    def name(self): ...
    def is_enabled_(self, args): ...
    def is_enabled(self): ...
    def is_visible_(self, args): ...
    def is_visible(self): ...
    def is_checked_(self, args): ...
    def is_checked(self): ...
    def description_(self, args): ...
    def description(self): ...
    def filter_args(self, args): ...
    def want_event(self): ...

class ApplicationCommand(Command):
    def run_(self, edit_token, args): ...
    def run(self): ...

class WindowCommand(Command):
    window = ...  # type: Any
    def __init__(self, window) -> None: ...
    def run_(self, edit_token, args): ...
    def run(self): ...

class TextCommand(Command):
    view = ...  # type: Any
    def __init__(self, view) -> None: ...
    def run_(self, edit_token, args): ...
    def run(self, edit): ...

class EventListener: ...

class ViewEventListener:
    @classmethod
    def is_applicable(cls, settings): ...
    @classmethod
    def applies_to_primary_view_only(cls): ...
    view = ...  # type: Any
    def __init__(self, view) -> None: ...

class TextInputHandler: ...

class ListInputHandler: ...

class MultizipImporter:
    loaders = ...  # type: Any
    file_loaders = ...  # type: Any
    def __init__(self) -> None: ...
    def find_module(self, fullname, path: Optional[Any] = ...): ...

class ZipLoader:
    zippath = ...  # type: Any
    name = ...  # type: Any
    def __init__(self, zippath) -> None: ...
    def has(self, fullname): ...
    def load_module(self, fullname): ...

override_path = ...  # type: Any
multi_importer = ...  # type: Any

def update_compressed_packages(pkgs): ...
def set_override_path(path): ...
