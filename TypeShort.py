import os
import re
import sublime
import sublime_plugin
from .functions import camel_to_snake
from .Globals import Globals
from .settings import get_package_name, get_setting


class TypeShortListener(sublime_plugin.EventListener):
    plugin_cmd = camel_to_snake(get_package_name())

    name_xml_regex = re.compile(r"<key>name</key>\s*<string>(?P<name>[^<>]*?)", re.DOTALL)
    name_yaml_regex = re.compile(r"^name\s*:\s*['\"]?(?P<name>.*)['\"]?(?=$|\s)", re.MULTILINE)

    def on_modified(self, view: sublime.View) -> None:
        # fix the issue that breaks functionality for undo/soft_undo
        history_cmd = view.command_history(1)
        if history_cmd[0] == self.plugin_cmd:
            return

        # no action if we are not typing
        history_cmd = view.command_history(0)
        if history_cmd[0] != "insert":
            return

        # get the last inserted chars
        # this could be more than one char sometimes somehow
        last_inserted_chars = history_cmd[1]["characters"]

        bindings = get_setting("bindings")
        current_syntaxes = self._get_current_syntaxes(view)

        for idx in range(0, len(bindings)):
            bindings[idx]["syntax_list"] = set(bindings[idx]["syntax_list"])

        jobs = [
            # {
            #     "region": [3, 6],
            #     "replacement": "$",
            # },
            # ...
        ]

        for region in view.sel():
            for binding in bindings:
                if (
                    # syntax matching
                    not (current_syntaxes & binding["syntax_list"])
                    # scope matching
                    and not any(
                        view.match_selector(region.begin(), syntax)
                        for syntax in binding["syntax_list"]
                    )
                ):
                    continue

                job = self._test_replace(view, region, binding, last_inserted_chars)

                if job:
                    jobs.append(job)

                    break

        if jobs:
            view.run_command(
                self.plugin_cmd,
                {"jobs": jobs, "cursor_placeholder": get_setting("cursor_placeholder")},
            )

    def _get_current_syntaxes(self, view: sublime.View) -> set:
        """
        @brief Get the syntax file name and the syntax name which is displayed on the bottom-right corner of ST.

        @param self The object
        @param view The view

        @return The current syntax.
        """

        syntax_file = view.settings().get("syntax")

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

    def _find_syntax_name(self, syntax_file: str):
        """
        @brief Find the name section in the give syntax file path.

        @param self        The object
        @param syntax_file The path of a syntax file

        @return Optional[str] The syntax name of `syntax_file` or None.
        """

        content = sublime.load_resource(syntax_file).strip()

        # .tmLanguage (XML)
        if content.startswith("<"):
            matches = self.name_xml_regex.search(content)
        # .sublime-syntax (YAML)
        else:
            matches = self.name_yaml_regex.search(content)

        return matches.group("name").strip() if matches else None

    def _test_replace(
        self, view: sublime.View, region: sublime.Region, binding: dict, last_inserted_chars: str
    ):
        """
        @brief Try to do replacement with given a binding and last inserted chars.

        @param self                The object
        @param view                The view
        @param region              The region
        @param binding             A binding in `bindings` in the settings file
        @param last_inserted_chars The last inserted characters

        @return Optional[dict]
        """

        for search, replacement in binding["keymaps"].items():
            # skip a keymap as early as possible
            if not (search.endswith(last_inserted_chars) or last_inserted_chars.endswith(search)):
                continue

            check_region = [region.begin() - len(search), region.end()]

            if view.substr(sublime.Region(*check_region)) == search:
                return {"region": check_region, "replacement": replacement}

        return None
