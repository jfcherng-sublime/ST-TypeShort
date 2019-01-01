from . import functions
import os
import re
import sublime
import sublime_plugin


PLUGIN_NAME = __package__
PLUGIN_DIR = "Packages/%s" % PLUGIN_NAME
PLUGIN_SETTINGS = PLUGIN_NAME + '.sublime-settings'
PLUGIN_CMD = functions.camelToSnake(PLUGIN_NAME)

settings = None

# {
#     syntaxFile: {
#         'fileName'  : '...',
#         'syntaxName': '...',
#     }
# }
syntaxInfos = {}


def plugin_loaded():
    global settings

    settings = sublime.load_settings(PLUGIN_SETTINGS)


class typeShortCommand(sublime_plugin.TextCommand):
    global settings

    def run(self, edit, regions=[], replacement=''):
        v = sublime.active_window().active_view()

        cursorPlaceholder = settings.get('cursor_placeholder', None)
        cursorFixedOffset = 0

        # validate the format of `replacement`
        if isinstance(cursorPlaceholder, str):
            cursorPlaceholderCount = replacement.count(cursorPlaceholder)

            # wrong usage
            if cursorPlaceholderCount > 1:
                print('[{}] ERROR: More than one cursor placeholder in `{}`'.format(PLUGIN_NAME, replacement))
                return False

            # correct usage
            if cursorPlaceholderCount == 1:
                cursorFixedOffset = replacement.index(cursorPlaceholder) + len(cursorPlaceholder) - len(replacement)
                replacement = replacement.replace(cursorPlaceholder, '', 1)

        # regions need to be replaced in a reversed sorted order
        for region in self.reverseSortRegions(regions):
            v.replace(
                edit,
                sublime.Region(region[0], region[1]),
                replacement
            )

            # correct cursor positions
            if cursorFixedOffset < 0:
                sels = v.sel()
                # remove the old cursor
                cursorPosition = region[0] + len(replacement)
                sels.subtract(sublime.Region(
                    cursorPosition,
                    cursorPosition
                ))
                # add a new cursor
                cursorPositionFixed = cursorPosition + cursorFixedOffset
                sels.add(sublime.Region(
                    cursorPositionFixed,
                    cursorPositionFixed
                ))

        return True

    def reverseSortRegions(self, regions):
        """
        sort `regions` in a descending order

        @param      self     The object
        @param      regions  A list of region which is in tuple form

        @return     `regions` in a descending order.
        """

        return sorted(regions, key=lambda region: region[0], reverse=True)


class typeShortListener(sublime_plugin.EventListener):
    global settings, syntaxInfos

    def __init__(self):
        self.sourceScopeRegex = re.compile(r'\b(?:source|text)\.[^\s]+')
        self.nameXmlRegex = re.compile(r'<key>name</key>\s*<string>(.*?)</string>', re.DOTALL)
        self.nameYamlRegex = re.compile(r'^name\s*:(.*)$', re.MULTILINE)

    def on_modified(self, view):
        """
        called after changes have been made to a view

        @param      self  The object
        @param      view  The view

        @return     True if a replacement happened, False otherwise.
        """

        v = sublime.active_window().active_view()

        # fix the issue that breaks functionality for undo/soft_undo
        historyCmd = v.command_history(1)
        if historyCmd[0] == PLUGIN_CMD:
            return False

        # no action if we are not typing
        historyCmd = v.command_history(0)
        if historyCmd[0] != 'insert':
            return False
        # get the last inserted chars
        lastInsertedChars = historyCmd[1]['characters']

        # collect scopes from the selection
        # we expect the fact that most regions would have the same scope
        scopesInSelection = {
            v.scope_name(region.begin()).rstrip()
            for region in v.sel()
        }

        # generate valid source scopes
        sourceScopes = (
            set(self.getCurrentSyntax(v)) |
            set(self.sourceScopeRegex.findall(' '.join(scopesInSelection)))
        )

        # try possible working bindings
        for binding in settings.get('bindings', []):
            if sourceScopes & set(binding['syntax_list']):
                success = self.doReplace(v, binding, lastInsertedChars)
                if success is True:
                    return True

        return False

    def getCurrentSyntax(self, view):
        """
        get the syntax file name and the syntax name which is on the
        bottom-right corner of ST

        @param      self  The object
        @param      view  The view

        @return     The current syntax.
        """

        syntaxFile = view.settings().get('syntax')

        if syntaxFile not in syntaxInfos:
            syntaxInfos[syntaxFile] = {
                'fileName': os.path.splitext(os.path.basename(syntaxFile))[0],
                'syntaxName': self.findSyntaxName(syntaxFile),
            }

        return [
            v
            for v in syntaxInfos[syntaxFile].values()
            if isinstance(v, str)
        ]

    def findSyntaxName(self, syntaxFile):
        """
        find the name section in the give syntax file path

        @param      self        The object
        @param      syntaxFile  The path of a syntax file

        @return     The syntax name of `syntaxFile` or None.
        """

        content = sublime.load_resource(syntaxFile).strip()

        # .tmLanguage (XML)
        if content.startswith('<'):
            matches = self.nameXmlRegex.search(content)
        # .sublime-syntax (YAML)
        else:
            matches = self.nameYamlRegex.search(content)

        if matches is None:
            return None

        return matches.group(1).strip()

    def doReplace(self, view, binding, lastInsertedChars):
        """
        try to do replacement with given a binding and last inserted chars

        @param      self               The object
        @param      view               The view object
        @param      binding            A binding in `bindings` in the settings
                                       file
        @param      lastInsertedChars  The last inserted characters

        @return     True/False on success/failure.
        """

        for search, replacement in binding['keymaps'].items():
            # skip a keymap as early as possible
            if not (
                search.endswith(lastInsertedChars) or
                lastInsertedChars.endswith(search)
            ):
                continue

            regionsToBeReplaced = []

            # iterate each region
            for region in view.sel():
                checkRegion = sublime.Region(
                    region.begin() - len(search),
                    region.end()
                )
                if view.substr(checkRegion) == search:
                    regionsToBeReplaced.append((
                        checkRegion.begin(),
                        checkRegion.end()
                    ))

            if regionsToBeReplaced:
                return view.run_command(PLUGIN_CMD, {
                    'regions': regionsToBeReplaced,
                    'replacement': replacement,
                })

        return True
