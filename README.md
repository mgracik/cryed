CryptoEditor
============

A simple wrapper around `openssl` for creating, viewing and editing encrypted
files.

CryptoEditor does not implement its own file editor, it uses the editor set in
the environment variable EDITOR. If you don't set the EDITOR variable, it will
try to use `vim`.

Installation
------------

`cd` into the project directory and run:

    make && sudo make install

Usage
-----

Viewing files:

    ccat <filename>

Editing files:

    cedit <filename>

Generate some random passphrases:

    ppgen
