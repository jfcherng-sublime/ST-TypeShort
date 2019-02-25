Sublime-TypeShort
=================

TypeShort is a snippet-like plugin for Sublime Text 3.
The original idea comes from [VvPhpDollar](https://github.com/ZhaonanLi/VvPhpDollar) by [ZhaonanLi](https://github.com/ZhaonanLi).
It will replace placeholders into corresponding replacements in real-time while typing.


Why This Plugin?
================

Do you ever consider `$`, `->`, `*`, `&`, etc to be uncomfortable to type?
Typing them usually requires you to move your fingers farther.

![screenshot](https://raw.githubusercontent.com/jfcherng/sublime-TypeShort/gh-pages/images/screenshot.gif)

Take the screenshot above as an example, you can set `fj_` 
(`_` represents a `space` here just for visibility) as a placeholder for `$` in PHP.
This plugin will automatically replace `fj_` with `$` in PHP whenever you type it.
Although `fj_` is 3-char, it could be typed faster than a `$` due to the normal keyboard layout.
You could also set `dk_` as a placeholder for `->` as well for the same reason.


Installation
============

Install using Package Control (Recommended), or by cloning this repository into the Packages directory.
Note that this plugin need you to set your own (`placeholder`, `replacement`) pairs to work properly.


Settings
========

This plugin does not have any default binding since it is very personal.
To add a binding, edit settings from the menu `Preferences » Package Settings » TypeShort » Settings`.


## Example settings

```javascript
{
    // This file is an example settings.
    // You should write your own settings in "Preferences » Package Settings » TypeShort » Settings - User"

    // the symbol used to represent the new cursor position after a replacement
    "cursor_placeholder": "{|}",

    // You can alternatively use either syntax file name, syntax name or scopes in the "syntax_list".
    // - syntax file name: The syntax file name without extension.
    // - syntax name: It's package-dependent and as shown on the bottom-right corner of your ST windows.
    // - scope: ctrl+alt+shift+p shows it which is in the form of "source.xxx/text.xxx".
    "bindings": [
        {
            // convert 'cmt ' into '<!--  -->' and place the cursor at its mid
            "keymaps": {
                "cmt ": "<!-- {|} -->"
            },
            // only works in HTML
            "syntax_list": ["text.html", "text.html.basic"]
        },
        {
            // convert 'fj ' into '$'
            // convert 'dk ' into '->'
            "keymaps": {
                "fj ": "$",
                "dk ": "->"
            },
            // only works in PHP
            "syntax_list": ["source.php"]
        },
        {
            // convert 'fj ' into '*'
            // convert 'dk ' into '->'
            "keymaps": {
                "fj ": "*",
                "dk ": "->"
            },
            // only works in C/C++
            "syntax_list": ["source.c", "source.c++", "source.c++11"]
        }
    ]
}
```


Supporters <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ATXYY9Y78EQ3Y" target="_blank"><img src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif" /></a>
==========

Thank you guys for sending me some cups of coffee.
