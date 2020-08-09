# A Lisp formatter

* Deterministic, like Black and Prettier!
* Tolerable defaults!
* Works with at least one Lisp dialect!

Nealean is a deterministic Lisp formatter.  It chops your source up and puts it back together again, better.

Install with:
```
pip3 install --user nelean
```

Uninstall with:
```
pip3 uninstall --user nelean
```

Use with Vim with [Neoformat](https://github.com/sbdchd/neoformat) with the hotkey "shift-L" with:
```
let g:neoformat_scheme_n = { 'exe': 'nelean', 'args': [], 'stdin': 1, 'replace': 0, 'valid_exit_codes': [0], }
let g:neoformat_enabled_scheme = ['n']
nnoremap L :Neoformat<Cr>
```

Nelean has no dependencies, so you can also just copy `nelean.py` somewhere in your `PATH`.

Additional options are availabile via the command line help.

The name comes from a famous professor of penmanship I found on Wikipedia, [D'Nelean](https://en.wikipedia.org/wiki/D%27Nealian).