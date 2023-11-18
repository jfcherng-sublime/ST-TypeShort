from __future__ import annotations

from dataclasses import asdict
from functools import lru_cache
from pathlib import Path

import sublime
import sublime_plugin

from .constant import PLUGIN_COMMAND
from .settings import get_setting
from .shared import G
from .types import CompiledBinding, ReplacementJob, ReplacementJobDict


@lru_cache
def _get_syntaxes_ids(syntax: sublime.Syntax) -> set[str]:
    return {Path(syntax.path).stem, syntax.name, syntax.scope} - {"", None}


class TypeShortListener(sublime_plugin.EventListener):
    def on_modified(self, view: sublime.View) -> None:
        if (
            # only work when the user was typing
            view.command_history(0)[0] != "insert"
            # fix the issue that breaks functionality for undo/soft_undo
            or view.command_history(1)[0] == PLUGIN_COMMAND
            # ...
            or not (syntax := view.syntax())
        ):
            return

        # jobs for the plugin command
        jobs: list[ReplacementJobDict] = []

        for region in view.sel():
            caret = region.b

            for binding in G.bindings:
                if (
                    # syntax matching such as "PHP"
                    (_get_syntaxes_ids(syntax) & binding.syntax_list)
                    # scope matching such as "source.php"
                    or view.match_selector(caret, binding.syntax_list_selector)
                ) and (job := self._test_point_with_binding(view, caret, binding)):
                    jobs.append(asdict(job))  # type: ignore
                    break

        if jobs:
            view.run_command(
                PLUGIN_COMMAND,
                {"jobs": jobs, "cursor_placeholder": get_setting("cursor_placeholder")},
            )

    def _test_point_with_binding(
        self,
        view: sublime.View,
        point: int,
        binding: CompiledBinding,
    ) -> ReplacementJob | None:
        # substr() the longest possible search to prevent from calling View API multiple times
        check_content = view.substr(sublime.Region(point - binding.keymaps_search_max_length, point))

        for search, replacement in binding.keymaps.items():
            search_length = len(search)
            if check_content[-search_length:] == search:
                return ReplacementJob(
                    region=(point - search_length, point),
                    replacement=replacement,
                )

        return None
