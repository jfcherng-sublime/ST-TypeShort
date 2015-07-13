"""
typeShort is a free software under MIT license.
This plugin allows you to set shortcuts for certain strings.

Copyright (c) 2015, jfcherng.
All rights reserved.
"""


import os
import sublime
import sublime_plugin


def Singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@Singleton
class typeShort():

    def __init__(self):
        self.SETTINGS_FILE_NAME = "TypeShort.sublime-settings"

        self.plugin_settings = sublime.load_settings(self.SETTINGS_FILE_NAME)
        self.plugin_settings.add_on_change("bindings", self.__refresh_settings)
        self.__refresh_settings()

    def __refresh_settings(self):
        self.bindings = self.plugin_settings.get("bindings", None)

    def do_replace(self, view, binding, lastInsertedChar):
        for search, replacement in binding['keymaps'].items():
            # skip a keymap as early as possible
            if not lastInsertedChar == search[-1]:
                continue
            # iterate each selection
            for editRegion in view.sel():
                checkRegion = sublime.Region(
                    editRegion.begin() - len(search),
                    editRegion.end()
                )
                if view.substr(checkRegion) == search:
                    view.run_command("type_short", {
                        "begin": checkRegion.begin(),
                        "end": checkRegion.end(),
                        "replacement": replacement
                    })
                    return True
        return False


class typeShortCommand(sublime_plugin.TextCommand):

    def run(self, edit, begin, end, replacement):
        self.view.replace(edit, sublime.Region(begin, end), replacement)


class typeShortListener(sublime_plugin.EventListener):

    def get_syntax(self, view):
        syntax = os.path.basename(view.settings().get("syntax"))
        syntax = os.path.splitext(syntax)[0]
        return syntax

    def on_modified(self, view):
        # Fix the issue that breaks functionality for Ctrl+Z
        historyCmd = view.command_history(1)
        if historyCmd[0] == 'type_short':
            return

        # Get the last press key
        historyCmd = view.command_history(0)
        if not historyCmd[0] == 'insert':
            return
        lastInsertedChar = historyCmd[1]['characters']

        obj = typeShort()
        currentSyntax = self.get_syntax(view)
        for binding in obj.bindings:
            if currentSyntax in binding['syntax_list']:
                replaced = obj.do_replace(view, binding, lastInsertedChar)
                if replaced is True:
                    break


def plugin_loaded():
    typeShort()
