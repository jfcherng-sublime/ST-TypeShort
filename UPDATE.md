TypeShort 1.2.0
===============

- Performance improvement for multiple cursors.
- Better undo/soft_undo behavior.
- Remove the `debug` option introduced in v1.1.1 since `ctrl+alt+shift+p` does it.


TypeShort 1.1.2
===============

- Fix a typo in `messages.json`.


TypeShort 1.1.1
===============

- Add `debug` options.

      Some packages' syntax is just not the same with the one shown in the
  bottom-right window of ST. By turning on the "debug" option of TypeShort,
  syntaxes/scopes match at current cursor will show in a popup message.

      For an example, while using the "Laravel Blade Highlighter" package, the
  bottom-right window of ST shows "Laravel Blade" but, in fact, its syntax is
  "blade".


TypeShort 1.1.0
===============

- Scopes can be used in `syntax_list` as well. (#1)

  You can alternatively use either syntaxes or scopes in the `syntax_list`.

  - Syntax: It's package-dependent and shown on the bottom-right corner of
            your ST windows.
  - Scope : It's in the form of `source.xxx` or `text.xxx`.
            You may check it with a plugin like `ScopeAlways` or `ScopeHunter`.


TypeShort 1.0.0
===============

- Initial release
