import os
import re
import sublime
import sublime_plugin
from .functions import camelcaseToUnderscore


PLUGIN_NAME = __package__
PLUGIN_DIR = "Packages/%s" % PLUGIN_NAME
PLUGIN_SETTINGS = PLUGIN_NAME + '.sublime-settings'
PLUGIN_CMD = camelcaseToUnderscore(PLUGIN_NAME)

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
    def run(self, edit, regions=[], replacement=''):
        # regions need to be replaced in a reversed sorted order
        regions = self.reverseSortRegions(regions)
        for region in regions:
            self.view.replace(
                edit,
                sublime.Region(region[0], region[1]),
                replacement
            )

    def reverseSortRegions(self, regions):
        """ sort regions in a descending order """

        return sorted(regions, key=lambda region: region[0], reverse=True)


class typeShortListener(sublime_plugin.EventListener):
    global settings, syntaxInfos

    def __init__(self):
        self.sourceScopeRegex = re.compile(r'\b(?:source|text)\.[^\s]+')
        self.nameXmlRegex = re.compile(r'<key>name</key>\s*<string>(.*?)</string>', re.DOTALL)
        self.nameYamlRegex = re.compile(r'^name\s*:(.*)$', re.MULTILINE)

    def on_modified(self, view):
        """ called after changes have been made to a view """

        # fix the issue that breaks functionality for undo/soft_undo
        historyCmd = view.command_history(1)
        if historyCmd[0] == PLUGIN_CMD:
            return

        # get the last press key
        historyCmd = view.command_history(0)
        if historyCmd[0] != 'insert':
            return
        lastInsertedStr = historyCmd[1]['characters']

        # collect scopes from the selection
        # we expect the fact that most regions would have the same scope
        scopesInSeletion = {
            view.scope_name(region.begin()).rstrip()
            for region in view.sel()
        }

        # generate valid source scopes
        sourceScopes = (
            set(self.getCurrentSyntax(view)) |
            set(self.sourceScopeRegex.findall(' '.join(scopesInSeletion)))
        )

        # try possible working bindings
        for binding in settings.get('bindings', []):
            if sourceScopes & set(binding['syntax_list']):
                success = self.doReplace(view, binding, lastInsertedStr)
                if success is True:
                    return

    def getCurrentSyntax(self, view):
        """ get the syntax file name and the syntax name which is on the bottom-right corner of ST """

        syntaxFile = view.settings().get('syntax')
        if syntaxFile not in syntaxInfos:
            syntaxInfos[syntaxFile] = {
                'fileName'   : os.path.splitext(os.path.basename(syntaxFile))[0],
                'syntaxName' : self.findSyntaxName(syntaxFile),
            }
        return [v for v in syntaxInfos[syntaxFile].values() if isinstance(v, str)]

    def findSyntaxName(self, syntaxFile):
        """ find the name section in the give syntax file path """

        content = sublime.load_resource(syntaxFile).strip()
        # .tmLanguage (XML)
        if content.startswith('<'):
            matches = self.nameXmlRegex.search(content)
        # .sublime-syntax (YAML)
        else:
            matches = self.nameYamlRegex.search(content)
        if matches is not None:
            return matches.group(1).strip()
        else:
            return None

    def doReplace(self, view, binding, lastInsertedStr):
        """ try to do replacement with given a binding and a last inserted char """

        for search, replacement in binding['keymaps'].items():
            # skip a keymap as early as possible
            if not (
                search.endswith(lastInsertedStr) or
                lastInsertedStr.endswith(search)
            ):
                continue
            # iterate each region
            regionsToBeReplaced = []
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
                view.run_command(PLUGIN_CMD, {
                    'regions'     : regionsToBeReplaced,
                    'replacement' : replacement,
                })
                return True
        return False
