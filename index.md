---
---

## ~~Literate~~ Literary Programming

Shakespeare Programming Language (SPL) is an esoteric language designed with the
goal of making its source code look like William Shakespeare's plays.

## History

SPL was designed by [Karl Wiberg](https://treskal.com/kha) and Jon Åslund in
2001. The documentation they made for it then [is still on the Internet](http://shakespearelang.sourceforge.net/report/shakespeare/shakespeare.html).
The specification came with a [reference implementation](http://shakespearelang.sf.net/download/spl-1.2.1.tar.gz),
an SPL-to-C source-to-source compiler. Over the years, other implementations have been made:

- [Lingua::Shakespeare](http://search.cpan.org/dist/Lingua-Shakespeare/lib/Lingua/Shakespeare.pod) in Perl
- [Spl](https://github.com/drsam94/Spl), an SPL-to-C in Python
- [horatio](https://github.com/mileszim/horatio), an interpreter in Javascript
- Probably others

I thought that the language was fun, but found it very frustrating to use these
compilers/interpreters because of the lack of immediate and helpful feedback
when things went wrong. SPL is a language *designed* to be almost impossible to
write, and searching for errors by making incremental changes to a program
makes it that much worse. For these reasons, I created my own implementation:

  - [shakespearelang](https://github.com/zmbc/shakespearelang), an interpreter in Python with a console and debugger

## Get Started

First, install the package from PyPI. It is called `shakespearelang`.

Then, create a new file called `first_program.spl` with this text:

```
A New Beginning.

Hamlet, a literary/storage device.
Juliet, an orator.

                    Act I: The Only Act.

                    Scene I: The Prince's Speech.

[Enter Hamlet and Juliet]

Juliet: Thou art the sum of an amazing healthy honest noble peaceful fine Lord
        and a lovely sweet golden summer's day. Speak your mind!

        Thou art the sum of thyself and a King. Speak your mind!

[Exeunt]
```

On the command line:

```
$ shakespeare run first_program.spl
HI
```

You just ran your first SPL program!

More coming soon...