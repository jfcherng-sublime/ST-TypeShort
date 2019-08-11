import sublime
import sublime_plugin
from .log import print_msg


class TypeShortCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit, jobs: list, cursor_placeholder: str = "{|}") -> bool:
        cursor_placeholder_len = len(cursor_placeholder)
        cursor_fixed_offset = 0

        # we process regions in reversed sorted order
        # so we do not have to recalculate region shift
        for job in sorted(jobs, key=lambda job: job["region"], reverse=True):
            region = job["region"]
            replacement = job["replacement"]

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

            self.view.replace(edit, sublime.Region(*region), replacement)

            # correct cursor positions
            if cursor_fixed_offset < 0:
                sels = self.view.sel()

                # remove the old cursor
                cursor_position = region[0] + len(replacement)
                sels.subtract(sublime.Region(cursor_position, cursor_position))

                # add a new cursor
                cursor_position_fixed = cursor_position + cursor_fixed_offset
                sels.add(sublime.Region(cursor_position_fixed, cursor_position_fixed))

        return True
