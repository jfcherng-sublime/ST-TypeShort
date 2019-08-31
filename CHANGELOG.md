# TypeShort


## 1.5.1

- Add and utilize the `typing` module.
- Changed plugin directory structure.


## 1.5.0

- Performance improvement.
- Allow using any selector in `syntax_list`.
  See https://www.sublimetext.com/docs/3/selectors.html for more information.


## 1.4.6

- Fix error message is not printed when there are more than 1 placeholder in the replacement.
- Split out `TypeShortCommand.py` from `TypeShort.py`.


## 1.4.5

- Fix a buggy typo which causes this plugin not to work in `Go` syntax.


## 1.4.4

- Just some refactors.


## 1.4.3

- [Fix] Replacement does not work in a new view of a file again.


## 1.4.2

- Use a new side-by-side window to edit settings.


## 1.4.1

- [Fix] Replacement does not work in a new view of a file.


## 1.4.0

- [Feature] Allow specifying the new cursor position after a replacement.


## 1.3.6

- Fix a bug introduced in `1.3.4`.


## 1.3.5

- Fix case problem introduced in `1.3.4` under non-Windows OS.


## 1.3.4

- Just some directory structure tweaks.


## 1.3.3

- Fix `historyEntry['characters']` may be longer than a single character. (SirNickolas)


## 1.3.2

- Minor performance improvement.


## 1.3.1

- Minor performance improvement.


## 1.3.0

- Syntax name can be used in `syntax_list` now.

      For an example, while using the `Laravel Blade Highlighter` package,
  `blade` (syntax file name), `text.blade` (scope) and `Laravel Blade`
  (syntax name, on the bottom-right corner of the ST window) are all working in
  the `syntax_list`.


## 1.2.1

- Fix a regex typo.


## 1.2.0

- Performance improvement for multiple cursors.
- Better undo/soft_undo behavior.
- Remove the `debug` option introduced in v1.1.1 since `ctrl+alt+shift+p` does it.


## 1.1.2

- Fix a typo in `messages.json`.


## 1.1.1

- Add `debug` options.

      Some packages' syntax is just not the same with the one shown in the
  bottom-right window of ST. By turning on the "debug" option of TypeShort,
  syntaxes/scopes match at current cursor will show in a popup message.

      For an example, while using the `Laravel Blade Highlighter` package, the
  bottom-right window of ST shows `Laravel Blade`. But, in fact, its syntax is
  `text.blade`.


## 1.1.0

- Scopes can be used in `syntax_list` as well. (#1)

  You can alternatively use either syntaxes or scopes in the `syntax_list`.

  - Syntax: It's package-dependent and shown on the bottom-right corner of
            your ST windows.
  - Scope : It's in the form of `source.xxx` or `text.xxx`.
            You may check it with a plugin like `ScopeAlways` or `ScopeHunter`.


## 1.0.0

- Initial release
