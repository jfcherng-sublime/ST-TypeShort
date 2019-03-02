from . import functions
import os
import re
import sublime
import sublime_plugin


PLUGIN_NAME = __package__
PLUGIN_DIR = "Packages/%s" % PLUGIN_NAME
PLUGIN_SETTINGS = '%s.sublime-settings' % PLUGIN_NAME
PLUGIN_CMD = functions.camel_to_snake(PLUGIN_NAME)


# Just a static cache.
#
# {
#     syntax_file: {
#         'file_name': '...',
#         'syntax_name': '...',
#     }
# }
syntax_infos = {}


class typeShortCommand(sublime_plugin.TextCommand):
    def run(self, edit, regions=[], replacement='', cursor_placeholder=''):
        v = sublime.active_window().active_view()

        cursor_placeholder_len = len(cursor_placeholder)
        cursor_fixed_offset = 0

        # adjustments about the cursor placeholder
        if cursor_placeholder_len > 0:
            cursor_placeholder_count = replacement.count(cursor_placeholder)

            # wrong usage
            if cursor_placeholder_count > 1:
                print('[{}] ERROR: More than one cursor placeholder in `{}`'.format(PLUGIN_NAME, replacement))

                return False

            # correct usage
            if cursor_placeholder_count == 1:
                cursor_fixed_offset = (
                    replacement.index(cursor_placeholder)
                    + cursor_placeholder_len
                    - len(replacement)
                )
                replacement = replacement.replace(cursor_placeholder, '', 1)

        # regions need to be replaced in a reversed sorted order
        for region in sorted(regions, reverse=True):
            v.replace(
                edit,
                sublime.Region(*region),
                replacement
            )

            # correct cursor positions
            if cursor_fixed_offset < 0:
                sels = v.sel()

                # remove the old cursor
                cursor_position = region[0] + len(replacement)
                sels.subtract(sublime.Region(
                    cursor_position,
                    cursor_position,
                ))

                # add a new cursor
                cursor_position_fixed = cursor_position + cursor_fixed_offset
                sels.add(sublime.Region(
                    cursor_position_fixed,
                    cursor_position_fixed,
                ))

        return True


class typeShortListener(sublime_plugin.EventListener):
    source_scope_regex = re.compile(r'\b(?:source|text)\.[^\s]+')
    name_xml_regex = re.compile(r'<key>name</key>\s*<string>(?P<name>.*?)</string>', re.DOTALL)
    name_yaml_regex = re.compile(r'^name\s*:(?P<name>.*)$', re.MULTILINE)

    def on_modified(self, view):
        """
        called after changes have been made to a view

        @param self The object
        @param view The view
        """

        settings = sublime.load_settings(PLUGIN_SETTINGS)
        v = sublime.active_window().active_view()

        # fix the issue that breaks functionality for undo/soft_undo
        history_cmd = v.command_history(1)
        if history_cmd[0] == PLUGIN_CMD:
            return

        # no action if we are not typing
        history_cmd = v.command_history(0)
        if history_cmd[0] != 'insert':
            return

        # get the last inserted chars
        # this could be more than one char sometimes somehow
        last_inserted_chars = history_cmd[1]['characters']

        # collect scopes from the selection
        # we expect the fact that most regions would have the same scope
        scopes_in_selection = {
            v.scope_name(region.begin()).rstrip()
            for region in v.sel()
        }

        # generate valid source scopes
        source_scopes = (
            set(self.get_current_syntax(v))
            | set(self.source_scope_regex.findall(' '.join(scopes_in_selection)))
        )

        # try possible working bindings
        for binding in settings.get('bindings', []):
            if (
                source_scopes & set(binding['syntax_list'])
                and self.do_replace(v, binding, last_inserted_chars)
            ):
                return

    def get_current_syntax(self, view):
        """
        get the syntax file name and the syntax name which is on the
        bottom-right corner of ST

        @param self The object
        @param view The view

        @return The current syntax.
        """

        global syntax_infos

        syntax_file = view.settings().get('syntax')

        if syntax_file not in syntax_infos:
            syntax_infos[syntax_file] = {
                'file_name': os.path.splitext(os.path.basename(syntax_file))[0],
                'syntax_name': self.find_syntax_name(syntax_file),
            }

        return [
            value
            for value in syntax_infos[syntax_file].values()
            if isinstance(value, str)
        ]

    def find_syntax_name(self, syntax_file):
        """
        find the name section in the give syntax file path

        @param self        The object
        @param syntax_file The path of a syntax file

        @return The syntax name of `syntax_file` or None.
        """

        content = sublime.load_resource(syntax_file).strip()

        # .tmLanguage (XML)
        if content.startswith('<'):
            matches = self.name_xml_regex.search(content)
        # .sublime-syntax (YAML)
        else:
            matches = self.name_yaml_regex.search(content)

        return None if matches is None else matches.group('name').strip()

    def do_replace(self, view, binding, last_inserted_chars):
        """
        try to do replacement with given a binding and last inserted chars

        @param self                The object
        @param view                The view object
        @param binding             A binding in `bindings` in the settings file
        @param last_inserted_chars The last inserted characters

        @return True/False on success/failure.
        """

        settings = sublime.load_settings(PLUGIN_SETTINGS)

        for search, replacement in binding['keymaps'].items():
            # skip a keymap as early as possible
            if not (
                search.endswith(last_inserted_chars)
                or last_inserted_chars.endswith(search)
            ):
                continue

            regions_to_be_replaced = []

            # iterate each region
            for region in view.sel():
                check_region = sublime.Region(
                    region.begin() - len(search),
                    region.end(),
                )

                if view.substr(check_region) == search:
                    regions_to_be_replaced.append((
                        check_region.begin(),
                        check_region.end(),
                    ))

            if regions_to_be_replaced:
                return view.run_command(PLUGIN_CMD, {
                    'regions': regions_to_be_replaced,
                    'replacement': replacement,
                    'cursor_placeholder': settings.get('cursor_placeholder', ''),
                })

        return False
