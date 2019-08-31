# Sublime-TypeShort

<a href="https://travis-ci.org/jfcherng/Sublime-TypeShort"><img alt="Travis (.org) branch" src="https://img.shields.io/travis/jfcherng/Sublime-TypeShort/master?style=flat-square"></a>
<a href="https://packagecontrol.io/packages/TypeShort"><img alt="Package Control" src="https://img.shields.io/packagecontrol/dt/TypeShort?style=flat-square"></a>
<a href="https://github.com/jfcherng/Sublime-TypeShort/tags"><img alt="GitHub tag (latest SemVer)" src="https://img.shields.io/github/tag/jfcherng/Sublime-TypeShort?style=flat-square&logo=github"></a>
<a href="https://github.com/jfcherng/Sublime-TypeShort/blob/master/LICENSE"><img alt="Project license" src="https://img.shields.io/github/license/jfcherng/Sublime-TypeShort?style=flat-square&logo=github"></a>
<a href="https://github.com/jfcherng/Sublime-TypeShort/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/jfcherng/Sublime-TypeShort?style=flat-square&logo=github"></a>
<a href="https://www.paypal.me/jfcherng/5usd" title="Donate to this project using Paypal"><img src="https://img.shields.io/badge/paypal-donate-blue.svg?style=flat-square&logo=paypal" /></a>

TypeShort is a snippet-like plugin for Sublime Text 3.
It replaces placeholders into corresponding replacements in real-time while typing.


## Why This Plugin?

Have you ever considered `$`, `->`, `*` or `&`, etc to be uncomfortable to type?
Typing them usually requires you to move your fingers farther.

![screenshot](https://raw.githubusercontent.com/jfcherng/sublime-TypeShort/gh-pages/images/screenshot.gif)
Oh, OOP PHP uses `$this->` so often... How long it takes you to type it?

Take the screenshot above as an example, you can set `fj█`
(`█` represents <kbd>space</kbd> here just for visibility) as a placeholder for `$` in PHP.
This plugin will automatically replace `fj█` with `$` in PHP whenever you type it.
Although `fj█` is 3-char, it can be typed faster than a single `$`
and you do not have to move any of your finger due to QWERTY keyboard layout.


## Installation

This package is available on Package Control by the name of [TypeShort](https://packagecontrol.io/packages/TypeShort).
Note that you have to set your own `(placeholder, replacement)` pairs to make this plugin work properly.


## Settings

This plugin does not have any default binding since obviously they are very personal.
To add a binding, edit settings from the menu `Preferences » Package Settings » TypeShort » Settings`.


### Example Settings

```javascript
{
    // This file is an example settings.
    // You should write your own settings in "Preferences » Package Settings » TypeShort » Settings"

    // the symbol used to represent the new cursor position after a replacement
    "cursor_placeholder": "{|}",

    // You can alternatively use either syntax file name, syntax name or scopes in the "syntax_list".
    // But scopes are recommended and the use of syntax (file) name may be removed in the future.
    //
    // - syntax file name: The syntax file name without extension.
    // - syntax name: It's package-dependent and as shown on the bottom-right corner of your ST windows.
    // - scope: ctrl+alt+shift+p shows it which usually starts with "source.xxx" or "text.xxx".
    //          You can use any ST selectors here. See https://www.sublimetext.com/docs/3/selectors.html
    "bindings": [
        {
            // only works in HTML
            "syntax_list": ["text.html.basic"],
            // convert 'cmt ' into '<!--  -->' and place the cursor at its mid
            "keymaps": {
                "cmt ": "<!-- {|} -->",
            },
        },
        {
            // only works in PHP
            "syntax_list": ["source.php"],
            // convert 'fj ' into '$'
            // convert 'dk ' into '->'
            "keymaps": {
                "fj ": "$",
                "dk ": "->",
            },
        },
        {
            // only works in C/C++
            "syntax_list": [
                "source.c", "source.c++",
                "source.objc", "source.objc++",
                "source.c++11", // C++11 package
            ],
            // convert 'fj ' into '*'
            // convert 'dk ' into '->',
            "keymaps": {
                "fj ": "*",
                "dk ": "->",
            },
        },
    ],
}
```
