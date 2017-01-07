shakespearelang
===============

An interpreter for the Shakespeare Programming Language, implemented in
Python.

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
executing, with features like a console and debugging. All previous
implementations of SPL were source-to-source-compilers, which makes an already
confusing language even harder to follow.

What state is this project in?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

I haven't written any tests yet, but it will *probably* run any valid
SPL program. The console and debugger are both working.

Installation
^^^^^^^^^^^^

.. code-block::

  pip install shakespearelang
  # Or however else you install things. You do you.

Instructions
^^^^^^^^^^^^

CLI
---

.. code-block::

  shakespeare run my-program.spl
  shakespeare debug my-program.spl
  shakespeare console # or just "shakespeare" unadorned

Console
-------

In the console, you'll essentially write an SPL program/play line-by-line,
defining your characters first.

Input to the console can be any of these:

- Entrances, exits, and spoken lines as they would normally appear in a play/program.
- Sentence(s) spoken by the last character who was speaking. For example,
  if the previous line was :code:`Juliet: You are a fat pig.`, the sentences
  :code:`Remember thyself! You are a fat fat pig.` could be tacked onto the
  previous line.
- Expressions (standalone values without assignment), spoken implicitly by the
  last speaking character or with an explicit character: :code:`Juliet: The difference between thyself and a fat pig`.
  These cannot end with periods.
- A character's name, which displays that character's stack and current value.
- :code:`stage`, which displays which characters are on and off stage.
- :code:`exit` or :code:`quit`, which will leave the console.

Debugging
---------

Debugging and running are identical for many programs. In order to utilize the
debugging feature, you'll need to place a breakpoint somewhere in your SPL code
using the following stage direction:

.. code-block::

  [A pause]

When the debugger hits this stage direction, it will *pause* execution of the play/program
and enter a REPL. This is just like the standalone console, except
you can use the :code:`next` command to step forward, and the :code:`continue`
command to exit the REPL and continue running the program/play.

.. _on Wikipedia: https://en.wikipedia.org/wiki/Shakespeare_Programming_Language
