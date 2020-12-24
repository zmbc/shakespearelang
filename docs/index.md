## Good morrow!

Welcome to the home of shakespearelang, a friendly interpreter for the Shakespeare
Programming Language (SPL) implemented in Python and available as a package on PyPI.
Aside from simply running programs, it also offers a console and debugger.

[The Shakespeare Programming Language](http://shakespearelang.sourceforge.net/)
(SPL) is an esoteric language with source code that looks like William
Shakespeare's plays. I take no credit for the language itself, which was designed
by [Karl Wiberg](https://treskal.com/kha) and Jon Åslund in 2001.

## Installation

`python -m pip install shakespearelang`

## Getting started

Create a new file called `first_play.spl` with this text:

```spl
A New Beginning.

Hamlet, a literary/storage device.
Juliet, an orator.

                    Act I: The Only Act.

                    Scene I: The Prince's Speech.

[Enter Hamlet and Juliet]

Juliet: Thou art the sum of an amazing healthy honest noble peaceful
        fine Lord and a lovely sweet golden summer's day. Speak your
        mind!

[A pause]

Juliet: Thou art the sum of thyself and a King. Speak your mind!

        Thou art the sum of an amazing healthy honest hamster and a golden
        chihuahua. Speak your mind!

[Exeunt]
```

In the terminal, use `shakespeare run` to run the play, like so:

```
$ shakespeare run first_play.spl
HI
```

If you see the output "HI", you just successfully ran your first SPL play!

## Debugging

For a guide to writing SPL plays, see [the original SPL documentation](http://shakespearelang.sourceforge.net/report/shakespeare/).

Written your play, but it's not working? shakespearelang tries to provide the
most useful error messages possible, but with a language designed to be almost
impossible to write, bugs are inevitable and an error message, if one is present,
isn't always enough.

### Activating the debugger

Remember the stage direction `[A pause]` in our `first_play.spl` file? That
special stage direction represents a breakpoint to the shakespearelang debugger.
To use the debugger, run the file again with the `debug` command, like so:

```
$ shakespeare debug first_play.spl
H

-----

Juliet: Thou art the sum of an amazing healthy honest noble peaceful
        fine Lord and a lovely sweet golden summer's day. Speak your
        mind!

> [A pause]

Juliet: Thou art the sum of thyself and a King. Speak your mind!

        Thou art the sum of an amazing healthy honest hamster and a golden

-----

>>
```

### Understanding the debugger

The "H" at the top is the first letter of output from our play. Then, the
stage direction causes the interpreter to pause. It shows us where in the play
it is--the line starting with `>` indicates the next line to run.

The last line (starting with `>>`) is a prompt, waiting for your input. This is
called the "console" or the ["REPL"](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop).

#### Lines

You can type any lines, entrances, and exits and they will be run as if they were in
the current scene. You cannot use the console to start new scenes or acts, nor
can you jump to another scene.

For example, you can increase Hamlet's value:

```
>> Juliet: Thou art the sum of thyself and a King.
Hamlet set to 73
>>
```

Having the speaking character's name at the beginning of the line is optional in
the console. Unattributed lines will be spoken by the last speaker.

```
>> Thou art a pig!
Hamlet set to -1
```

#### Expressions

In addition to normal lines, the console also accepts standalone expressions,
the result of which it displays. These cannot end with periods. The answers
to questions are also displayed.

```
>> Juliet: The sum of thyself and a King
74
>> Juliet: Are you nicer than a golden chihuahua?
True
>>
```

#### Inspecting the stage and characters

To see a list of characters currently on stage, enter `stage` into the console.

```
>> stage
On stage:
Hamlet
Juliet

Off stage:
```

To inspect a character, simply enter their name.

```
>> Hamlet
Hamlet
Value: 74
Stack:
>> Juliet: Remember thyself!
Hamlet pushed 74
>> Hamlet
Hamlet
Value: 74
Stack:
74
>>
```

#### Commands

The commands `next` and `continue` are special. `next` executes the next line or
event in the play, returning you to the interactive console afterwards. `continue`
simply continues running the play--it will not stop again unless it hits another
breakpoint.

## Console

If you don't have a play yet and just want to mess around, you can open the
console in the context of an empty play with the `shakespeare console` command,
or simply `shakespeare`.

## Other implementations

shakespearelang is not the only implementation of SPL, though it aims to be the
friendliest.

Other options:

- [The reference implementation](http://shakespearelang.sf.net/download/spl-1.2.1.tar.gz),
an SPL-to-C source-to-source compiler
- [Lingua::Shakespeare](http://search.cpan.org/dist/Lingua-Shakespeare/lib/Lingua/Shakespeare.pod), a source filter in Perl
- [Spl](https://github.com/drsam94/Spl), an SPL-to-C compiler in Python
- [horatio](https://github.com/mileszim/horatio), an interpreter in Javascript
