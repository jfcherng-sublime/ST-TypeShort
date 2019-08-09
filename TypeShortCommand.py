import sublime
import sublime_plugin
from .log import print_msg


class TypeShortCommand(sublime_plugin.TextCommand):
    def run(
        self,
        edit: sublime.Edit,
        regions: list = [],
        replacement: str = "",
        cursor_placeholder: str = "{|}",
    ) -> bool:
        v = sublime.active_window().active_view()

        cursor_placeholder_len = len(cursor_placeholder)
        cursor_fixed_offset = 0

        # adjustments about the cursor placeholder
        if cursor_placeholder_len > 0:
            cursor_placeholder_count = replacement.count(cursor_placeholder)

            # wrong usage
            if cursor_placeholder_count > 1:
                print_msg("ERROR: More than one cursor placeholder in `{}`".format(replacement))

                return False

            # correct usage
            if cursor_placeholder_count == 1:
                cursor_fixed_offset = (
                    replacement.index(cursor_placeholder)
                    + cursor_placeholder_len
                    - len(replacement)
                )
                replacement = replacement.replace(cursor_placeholder, "", 1)

        # regions need to be replaced in a reversed sorted order
        for region in sorted(regions, reverse=True):
            v.replace(edit, sublime.Region(*region), replacement)

            # correct cursor positions
            if cursor_fixed_offset < 0:
                sels = v.sel()

                # remove the old cursor
                cursor_position = region[0] + len(replacement)
                sels.subtract(sublime.Region(cursor_position, cursor_position))

                # add a new cursor
                cursor_position_fixed = cursor_position + cursor_fixed_offset
                sels.add(sublime.Region(cursor_position_fixed, cursor_position_fixed))

        return True
