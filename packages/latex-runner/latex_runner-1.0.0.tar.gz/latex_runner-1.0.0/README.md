# latex-runner

A wrapper around LaTeX to build files which

- reads [magic comments](#magic-comments) to determine the TeX program and options to be used.
- filters the output to show only errors, warnings, over-/underfull boxes, tracing commands and prompts.
- runs [biber](https://ctan.org/pkg/biber) and [makeglossaries](https://ctan.org/pkg/glossaries) if necessary.
- reruns LaTeX up to -n times if necessary.


## Magic Comments

This program supports the following [magic comments](https://texstudio-org.github.io/advanced.html#advanced-header-usage):

```tex
% !TeX root = ../main.tex
```

Run the TeX program with the given file instead.
This is useful if you have split up your document into multiple files, the current file is included in the main file with [`\input` or `\include`](https://tex.stackexchange.com/questions/246/when-should-i-use-input-vs-include) and you have told vim to build the currently opened file with this program.


```tex
% !TeX program = pdflatex
```

The program used to build the tex file.

For security reasons programs *not* listed in the `allowed-tex-programs` setting are *not* executed.
By default the allowed programs are `pdflatex`, `xelatex`, `lualatex`, `latex`, `tex` and `pdftex`.
You can change these with `latex-runner --edit-config`.


```tex
% !TeX option = -shell-escape
```

A command line option which should be passed to the TeX program.
You can repeat this comment to enable several command line options.
I have introduced this type of comment because at the time of this writing `% !TeX program = pdflatex -shell-escape` breaks compilation in [TeX studio](https://www.texstudio.org/).

For security reasons options *not* listed in the `allowed-tex-options` setting are *not* passed to the TeX program.
By default the allowed options are `--shell-escape`, `--8bit`, `--interaction=batchmode`, `--interaction=nonstopmode`, `--interaction=scrollmode` and `--interaction=errorstopmode`.
You can change these with `latex-runner --edit-config`.


## Config

You can change settings with

```bash
latex-runner --edit-config
```

You can get help how to configure this program with

```bash
latex-runner --help-config
```


## Installation

You can install this program via the python package manager [pipx](https://pipx.pypa.io/latest/):

```bash
pipx install latex-runner
```


## vim integration

Copy the following into `~/.vim/after/ftplugin/tex.vim`.
This will allow you to run LaTeX once with F5, build the pdf completely with Control+F5 and open the pdf at the cursor position in [zathura](https://pwmt.org/projects/zathura/) with Shift+F5 or F6. You can open the log file with F7.

```vim
" build pdf
nnoremap <buffer> <F5> :exec "!latex-runner -n1 -synctex=1 " .. expand('%:p:S')<cr>
nnoremap <buffer> <C-F5> :exec "!latex-runner -n5 -synctex=1 " .. expand('%:p:S')<cr>

" open pdf
nnoremap <buffer> <S-F5> :exec "silent! !zathura --synctex-forward " .. line('.') .. ":" .. col('.') .. ":" .. expand('%:p') .. " " .. trim(system('latex-runner --get-pdf ' .. expand('%:p:S') .. " 2>/dev/null")) .. " >/dev/null 2>/dev/null &"<cr>:redraw!<cr>
nnoremap <buffer> <F6> :exec "silent! !zathura --synctex-forward " .. line('.') .. ":" .. col('.') .. ":" .. expand('%:p') .. " " .. trim(system('latex-runner --get-pdf ' .. expand('%:p:S') .. " 2>/dev/null")) .. " >/dev/null 2>/dev/null &"<cr>:redraw!<cr>

" open log file, return with :bp
nnoremap <buffer> <F7> :exec "edit " .. trim(system('latex-runner --get-log ' .. expand('%:p:S') .. " 2>/dev/null"))<cr>

" texdoc, to be used when cursor is in argument of \usepackage
nnoremap <buffer> K :silent exec '!texdoc <c-r>=expand("<cfile>")<cr> >/dev/null 2>&1 &' \| redraw!<cr>

" inserting magic comments
command InsertMagicCommentXelatex     :0put ='% !TeX program = xelatex'
command InsertMagicCommentPdflatex    :0put ='% !TeX program = pdflatex'
command InsertMagicCommentShellEscape :1put ='% !TeX option = -shell-escape'
command InsertMagicCommentRoot        :0put ='% !TeX root = ../main.tex'
```

## Running the tests

I am using [mypy](https://www.mypy-lang.org/) for static type checking and [pytest](https://docs.pytest.org/en/latest/) for dynamic testing.
[tox](https://tox.wiki/en/latest/) creates a virtual environment and installs all dependencies for you.
You can install tox with [pipx](https://pypa.github.io/pipx/) (`pipx install tox`).

```bash
$ tox
```

In order to make tox work without an internet connection install [devpi](https://devpi.net/docs/devpi/devpi/stable/%2Bd/index.html):

```bash
$ pipx install devpi-server
$ devpi-init
$ devpi-gen-config
$ su
# cp gen-config/devpi.service /etc/systemd/system/
# systemctl start devpi.service
# systemctl enable devpi.service
```

and add the following line to your bashrc:

```bash
export PIP_INDEX_URL=http://localhost:3141/root/pypi/+simple/
```
