import os
import re
import sublime
import sublime_plugin
from typing import Any, List, Dict, Set, Optional
from ..functions import camel_to_snake
from ..Globals import Globals
from ..settings import get_package_name, get_setting


class TypeShortListener(sublime_plugin.EventListener):
    plugin_cmd = camel_to_snake(get_package_name())

    name_xml_regex = re.compile(r"<key>name</key>\s*<string>(?P<name>[^<>]*?)", re.DOTALL)
    name_yaml_regex = re.compile(r"^name\s*:\s*['\"]?(?P<name>.*)['\"]?\s*$", re.MULTILINE)

    def on_modified(self, view: sublime.View) -> None:
        # only work when the user was typing
        if view.command_history(0)[0] != "insert":
            return

        # fix the issue that breaks functionality for undo/soft_undo
        if view.command_history(1)[0] == self.plugin_cmd:
            return

        # jobs for the plugin command
        jobs = [
            # {
            #     "region": [3, 6],
            #     "replacement": "$",
            # },
            # ...
        ]  # type: List[Dict[str, Any]]

        for region in view.sel():  # type: ignore
            point = region.begin()

            for binding in Globals.bindings:
                if (
                    # syntax matching such as "PHP"
                    (self._get_current_syntaxes(view) & binding["syntax_list"])
                    # scope matching such as "source.php"
                    or view.match_selector(point, binding["syntax_list_selector"])
                ):
                    job = self._test_point_with_binding(view, point, binding)

                    if job:
                        jobs.append(job)

                        break

        if jobs:
            # fmt: off
            view.run_command(
                self.plugin_cmd,
                {"jobs": jobs, "cursor_placeholder": get_setting("cursor_placeholder")},
            )
            # fmt: on

    def _test_point_with_binding(self, view: sublime.View, point: int, binding: dict) -> Optional[Dict]:
        """
        @brief Test whether the binding can be applied to the point.

        @param self    The object
        @param view    The view
        @param point   The point
        @param binding The binding

        @return Optional[dict] The job for plugin command if there is a matching one
        """

        # substr() the longest possible search to prevent from calling View API multiple times
        check_content = view.substr(sublime.Region(point - binding["keymaps_search_max_length"], point))

        for search, replacement in binding["keymaps"].items():
            search_length = len(search)

            if check_content[-search_length:] == search:
                return {"region": [point - search_length, point], "replacement": replacement}

        return None

    def _get_current_syntaxes(self, view: sublime.View) -> Set:
        """
        @brief Get the syntax file name and the syntax name which is displayed
               on the bottom-right corner of ST.

        @param self The object
        @param view The view

        @return The current syntax.
        """

        syntax_file = str(view.settings().get("syntax"))

        if syntax_file not in Globals.syntax_infos:
            file_basename = os.path.basename(syntax_file)
            file_name, file_ext = os.path.splitext(file_basename)

            # the syntax name displayed on the bottom-right corner of ST
            syntax_name = self._find_syntax_name(syntax_file) or ""

            # in case there is an empty one
            syntax_ids = set([file_name, syntax_name]) - set([""])

            Globals.syntax_infos[syntax_file] = {
                "file_basename": file_basename,
                "file_ext": file_ext,  # with dot
                "file_name": file_name,  # no ext
                "file_path": syntax_file,
                "syntax_name": syntax_name,
                "syntax_ids": syntax_ids,  # names represent this syntax
            }

        return Globals.syntax_infos[syntax_file]["syntax_ids"]

    def _find_syntax_name(self, syntax_file: str) -> Optional[str]:
        """
        @brief Find the name section in the give syntax file path.

        @param self        The object
        @param syntax_file The path of a syntax file

        @return Optional[str] The syntax name of the `syntax_file` if found.
        """

        content = sublime.load_resource(syntax_file).strip()

        # .tmLanguage (XML)
        if content.startswith("<"):
            matches = self.name_xml_regex.search(content)
        # .sublime-syntax (YAML)
        else:
            matches = self.name_yaml_regex.search(content)

        return matches.group("name").strip() if matches else None
