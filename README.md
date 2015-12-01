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
```javascript
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
```javascript
{
    // This file is an example settings.
    // You should write your own settings in "Preferences » Package Settings » TypeShort » Settings - User"

    // You can alternatively use either syntaxes or scopes in the "syntax_list".
    //     syntax: it's package-dependent and shown in the bottom-right corner of your ST windows
    //     scope : it's in the form of source.xxx
    //             you may check it with a plugin like ScopeAlways or ScopeHunter

    "bindings": [
        {
            // convert 'fj ' into '$'
            // convert 'dk ' into '->'
            "keymaps": {
                "fj ": "$",
                "dk ": "->"
            },
            // only work in PHP
            "syntax_list": ["source.php"]
        },
        {
            // convert 'fj ' into '*'
            // convert 'dk ' into '->'
            "keymaps": {
                "fj ": "*",
                "dk ": "->"
            },
            // only work in C/C++
            "syntax_list": ["source.c", "source.c++", "source.c++11"]
        }
    ]
}
```
