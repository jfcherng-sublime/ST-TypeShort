# TypeShort #

TypeShort is a snippet-like plugin for Sublime Text 3.

The original idea comes from [VvPhpDollar](https://github.com/ZhaonanLi/VvPhpDollar) by [ZhaonanLi](https://github.com/ZhaonanLi).

It will replace placeholders into corresponding replacements in real-time while typing.


## Usage ##

For example, typing a `$` or a `->` in PHP may be just not that comfortable.

You can set `fj_` (`_` means a space here, just for interpretation) as a placeholder for `$` in PHP.

This plugin will automatically replace `fj_` into `$` in PHP whenever you type it.

Although `fj_` has three characters, it could still be typed faster than a `$`.


## Screenshot(s) ##

![](https://raw.githubusercontent.com/jfcherng/sublime-TypeShort/gh-pages/images/screenshot.gif)


## Installation ##

Install using Package Control (Recommended), or by cloning this repository into the Packages directory.

Note that this plugin need you to set your own (`placeholder`, `replacement`) pairs to work properly.


## Settings ##

Edit settings from the menu `Preferences » Package Settings » TypeShort » Settings - User`.

Settings structure:
```json
{
    "bindings": [
        {
            "keymaps": {
                "placeholder_1": "replacement_1",
                "placeholder_2": "replacement_2"
                ...
            },
            "syntax_list": ["syntax_1", "syntax_2", ...]
        },
        ...
    ]
}
```

Example settings:
```json
{
    "bindings": [
        {
            "keymaps": {
                "fj ": "$",
                "dk ": "->"
            },
            "syntax_list": ["PHP"]
        },
        {
            "keymaps": {
                "fj ": "*",
                "dk ": "->"
            },
            "syntax_list": ["C", "C++", "C++11", "C#", "Objective-C", "Objective-C++"]
        }
    ]
}
```
