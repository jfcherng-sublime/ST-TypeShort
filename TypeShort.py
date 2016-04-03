import os
import re
import sublime
import sublime_plugin


PLUGIN_NAME = 'TypeShort'
PLUGIN_DIR = "Packages/%s" % PLUGIN_NAME
PLUGIN_SETTINGS = PLUGIN_NAME + '.sublime-settings'

settings = None


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
    global settings

    def __init__(self):
        self.sourceRegex = re.compile(r'\b(?:source|text)\.[^\s]+')

    def on_modified(self, view):
        """ called after changes have been made to a view """

        # fix the issue that breaks functionality for undo/soft_undo
        historyCmd = view.command_history(1)
        if historyCmd[0] == 'type_short':
            return

        # get the last press key
        historyCmd = view.command_history(0)
        if historyCmd[0] != 'insert':
            return
        lastInsertedChar = historyCmd[1]['characters']

        # collect scopes from the selection
        scopes = { self.getSyntax(view) }
        for region in view.sel():
            scopes |= set(self.sourceRegex.findall(view.scope_name(region.begin())))

        # try possible working bindings
        for binding in settings.get('bindings', []):
            if scopes & set(binding['syntax_list']):
                success = self.doReplace(view, binding, lastInsertedChar)
                if success is True:
                    return

    def getSyntax(self, view):
        """ get the syntax file name which is usually on the bottom-right corner of ST """

        return os.path.splitext(os.path.basename(view.settings().get('syntax')))[0]

    def doReplace(self, view, binding, lastInsertedChar):
        for search, replacement in binding['keymaps'].items():
            # skip a keymap as early as possible
            if lastInsertedChar != search[-1]:
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
                view.run_command('type_short', {
                    'regions': regionsToBeReplaced,
                    'replacement': replacement
                })
                return True
        return False
