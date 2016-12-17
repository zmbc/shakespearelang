shakespearelang
===============

An interpreter for the Shakespeare Programming Language, implemented in
Python.

How do I get this?
^^^^^^^^^^^^^^^^^^

.. code-block::

  pip install shakespearelang`

How do I use this?
^^^^^^^^^^^^^^^^^^

Running a file:

.. code-block::

  shakespeare run file-name

Entering a REPL/console:

.. code-block::

  shakespeare repl
  # or
  shakespeare

What is the Shakespeare Programming Language?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Shakespeare Programming Language (SPL) is a programming language
with source code that looks like Shakespeare's plays. The language is
Turing complete, so theoretically just as powerful as any other
language. It's a lot of fun to write but not practical for any large
projects. More info can be found `on Wikipedia`_.

Note: Shakespeare's actual plays are not valid SPL. SPL does not aim to
provide backwards compatibility with legacy code written ~400 years ago.

What is this project?
^^^^^^^^^^^^^^^^^^^^^

This is an interpreter I wrote for SPL. It's written in Python. The aim
is to help programmers better understand how their SPL code is
executing, with features like REPL and debugging. All previous
implementations of SPL were cross-compilers, which makes an already
confusing language even harder to follow.

What state is this project in?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

I haven't written any tests yet, but it will *probably* run any valid
SPL program. Try running

.. code-block::

  shakespeare repl
  # or
  shakespeare

to play with a fun REPL. Debugging is coming Soon :superscript:`TM`.

.. _on Wikipedia: https://en.wikipedia.org/wiki/Shakespeare_Programming_Language
