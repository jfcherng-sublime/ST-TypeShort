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
    def run(self, edit, begin, end, replacement):
        self.view.replace(edit, sublime.Region(begin, end), replacement)


class typeShortListener(sublime_plugin.EventListener):
    global settings

    def __init__(self):
        self.sourceRegex = re.compile(r'\b(?:source|text).[^\s]+')

    def on_modified(self, view):
        """ called after changes have been made to a view """

        # fix the issue that breaks functionality for Ctrl+Z
        historyCmd = view.command_history(1)
        if historyCmd[0] == 'type_short':
            return

        # get the last press key
        historyCmd = view.command_history(0)
        if historyCmd[0] != 'insert':
            return
        lastInsertedChar = historyCmd[1]['characters']

        # collect scopes from selections
        scopes = set()
        for region in view.sel():
            scopes |= set(self.sourceRegex.findall(view.scope_name(region.begin())))
        # add the current syntax into scopes
        scopes.add(self.getSyntax(view))

        for binding in settings.get('bindings', []):
            if scopes.intersection(set(binding['syntax_list'])):
                replaced = self.doReplace(view, binding, lastInsertedChar)
                if replaced is True:
                    return

    def getSyntax(self, view):
        """ get the syntax which is on the bottom-right corner of ST """

        return os.path.splitext(os.path.basename(view.settings().get('syntax')))[0]

    def doReplace(self, view, binding, lastInsertedChar):
        replaced = False
        for search, replacement in binding['keymaps'].items():
            # skip a keymap as early as possible
            if lastInsertedChar != search[-1]:
                continue
            # iterate each selection
            for region in view.sel():
                checkRegion = sublime.Region(
                    region.begin() - len(search),
                    region.end()
                )
                if view.substr(checkRegion) == search:
                    replaced = True
                    view.run_command('type_short', {
                        'begin': checkRegion.begin(),
                        'end': checkRegion.end(),
                        'replacement': replacement
                    })
            if replaced is True:
                break
        return replaced
