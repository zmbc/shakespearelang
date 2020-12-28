from ..shakespeare_interpreter import Shakespeare
from io import StringIO

class TestSamplePrograms:
    def test_runs_hi(self, capsys):
        Shakespeare().run_play("""
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
        """)
        captured = capsys.readouterr()
        assert captured.out == 'HI\n'
        assert captured.err == ''

    def test_runs_hello_world(self, capsys):
        Shakespeare().run_play("""
            The Infamous Hello World Program.

            Romeo, a young man with a remarkable patience.
            Juliet, a likewise young woman of remarkable grace.
            Ophelia, a remarkable woman much in dispute with Hamlet.
            Hamlet, the flatterer of Andersen Insulting A/S.


                                Act I: Hamlet's insults and flattery.

                                Scene I: The insulting of Romeo.

            [Enter Hamlet and Romeo]

            Hamlet:
             You lying stupid fatherless big smelly half-witted coward!
             You are as stupid as the difference between a handsome rich brave
             hero and thyself! Speak your mind!

             You are as brave as the sum of your fat little stuffed misused dusty
             old rotten codpiece and a beautiful fair warm peaceful sunny summer's
             day. You are as healthy as the difference between the sum of the
             sweetest reddest rose and my father and yourself! Speak your mind!

             You are as cowardly as the sum of yourself and the difference
             between a big mighty proud kingdom and a horse. Speak your mind.

             Speak your mind!

            [Exit Romeo]

                                Scene II: The praising of Juliet.

            [Enter Juliet]

            Hamlet:
             Thou art as sweet as the sum of the sum of Romeo and his horse and his
             black cat! Speak thy mind!

            [Exit Juliet]

                                Scene III: The praising of Ophelia.

            [Enter Ophelia]

            Hamlet:
             Thou art as lovely as the product of a large rural town and my amazing
             bottomless embroidered purse. Speak thy mind!

             Thou art as loving as the product of the bluest clearest sweetest sky
             and the sum of a squirrel and a white horse. Thou art as beautiful as
             the difference between Juliet and thyself. Speak thy mind!

            [Exeunt Ophelia and Hamlet]


                                Act II: Behind Hamlet's back.

                                Scene I: Romeo and Juliet's conversation.

            [Enter Romeo and Juliet]

            Romeo:
             Speak your mind. You are as worried as the sum of yourself and the
             difference between my small smooth hamster and my nose. Speak your
             mind!

            Juliet:
             Speak YOUR mind! You are as bad as Hamlet! You are as small as the
             difference between the square of the difference between my little pony
             and your big hairy hound and the cube of your sorry little
             codpiece. Speak your mind!

            [Exit Romeo]

                                Scene II: Juliet and Ophelia's conversation.

            [Enter Ophelia]

            Juliet:
             Thou art as good as the quotient between Romeo and the sum of a small
             furry animal and a leech. Speak your mind!

            Ophelia:
             Thou art as disgusting as the quotient between Romeo and twice the
             difference between a mistletoe and an oozing infected blister! Speak
             your mind!

            [Exeunt]
        """)
        captured = capsys.readouterr()
        assert captured.out == 'Hello World!\n'
        assert captured.err == ''

    def test_runs_catch(self, capsys):
        Shakespeare().run_play("""
            A Program to Woo the People.

            Tybalt, an orator.
            Macbeth, a literary/storage device.

                Act I: The Only Act.

                Scene I: The Prince's Speech.

            [Enter Macbeth and Tybalt]

            Tybalt: Thou art the sum of an amazing healthy honest noble peaceful fine Lord and the sum of a golden king and a lord.  Speak your mind!

            Macbeth: Remember me!

            Tybalt: Thou art the sum of thyself and a smelly beggar. Speak your mind!

            Macbeth: Thou art the sum of a warm healthy amazing noble peaceful fine lord and the sum of a golden peaceful smooth amazing king and a golden healthy lord. Speak your mind!

            Macbeth: Recall your imminent demise! Speak your mind!

            Tybalt: You are as good as the sum of a golden warm healthy amazing noble fine lord and a golden good healthy king! Speak your mind!
        """)
        captured = capsys.readouterr()
        assert captured.out == 'CATCH'
        assert captured.err == ''

    def test_runs_echo(self, monkeypatch, capsys):
        monkeypatch.setattr('sys.stdin', StringIO('m123cfoobar123'))
        Shakespeare().run_play("""
            A rose by any other name.
            Romeo, a speaker.
            Juliet, his muse.
                       Act I: Something.
                       Scene I: A garden.
            [Enter Romeo and Juliet]
            Romeo: Open your mind! Speak your mind!
            Romeo: Listen to your heart! Open your heart!
            Romeo: Open your mind! Speak your mind!
            [Exeunt]
        """)
        captured = capsys.readouterr()
        assert captured.out == 'm123c'
        assert captured.err == ''

    def test_runs_primes(self, monkeypatch, capsys):
        monkeypatch.setattr('sys.stdin', StringIO('20'))
        Shakespeare().run_play("""
            Prime Number Computation in Copenhagen.

            Romeo, a young man of Verona.
            Juliet, a young woman.
            Hamlet, a temporary variable from Denmark.
            The Ghost, a limiting factor (and by a remarkable coincidence also
                    Hamlet's father).


                                Act I: Interview with the other side.

                                Scene I: At the last hour before dawn.

            [Enter the Ghost and Juliet]

            The Ghost:
             You pretty little warm thing! Thou art as prompt as the difference
             between the square of thyself and your golden hair. Speak your mind.

            Juliet:
             Listen to your heart!

            [Exit the Ghost]

            [Enter Romeo]

            Juliet:
             Thou art as sweet as a sunny summer's day!


                                Act II: Determining divisibility.

                                Scene I: A private conversation.

            Juliet:
             Art thou more cunning than the Ghost?

            Romeo:
             If so, let us proceed to scene V.

            [Exit Romeo]

            [Enter Hamlet]

            Juliet:
             You are as villainous as the square root of Romeo!

            Hamlet:
             You are as lovely as a red rose.

                                Scene II: Questions and the consequences thereof.

            Juliet:
             Am I better than you?

            Hamlet:
             If so, let us proceed to scene III.

            Juliet:
             Is the remainder of the quotient between Romeo and me as good as
             nothing?

            Hamlet:
             If so, let us proceed to scene IV.
             Thou art as bold as the sum of thyself and a roman.

            Juliet:
             Let us return to scene II.

                                Scene III: Romeo must die!

            [Exit Hamlet]

            [Enter Romeo]

            Juliet:
             Open your heart.

            [Exit Juliet]

            [Enter Hamlet]

            Romeo:
             Thou art as rotten as the difference between nothing and the sum of a
             snotty stinking half-witted hog and a small toad!
             Speak your mind!

            [Exit Romeo]

            [Enter Juliet]

                                Scene IV: One small dog at a time.

            [Exit Hamlet]

            [Enter Romeo]

            Juliet:
             Thou art as handsome as the sum of thyself and my chihuahua!
             Let us return to scene I.

                                Scene V: Fin.

            [Exeunt]
        """)
        captured = capsys.readouterr()
        assert captured.out == '>2\n3\n5\n7\n11\n13\n17\n19\n'
        assert captured.err == ''

    def test_runs_reverse(self, monkeypatch, capsys):
        monkeypatch.setattr('sys.stdin', StringIO('first\nsecond\nthird'))
        Shakespeare().run_play("""
            Outputting Input Reversedly.

            Othello, a stacky man.
            Lady Macbeth, who pushes him around till he pops.


                                Act I: The one and only.

                                Scene I: In the beginning, there was nothing.

            [Enter Othello and Lady Macbeth]

            Othello:
             You are nothing!

                                Scene II: Pushing to the very end.

            Lady Macbeth:
             Open your mind! Remember yourself.

            Othello:
             You are as hard as the sum of yourself and a stone wall. Am I as
             horrid as a flirt-gill?

            [A pause]

            Lady Macbeth:
             If not, let us return to scene II. Recall your imminent death!

            Othello:
             You are as small as the difference between yourself and a hair!

                                Scene III: Once you pop, you can't stop!

            Lady Macbeth:
             Recall your unhappy childhood. Speak your mind!

            Othello:
             You are as vile as the sum of yourself and a toad! Are you better
             than nothing?

            Lady Macbeth:
             If so, let us return to scene III.

                                Scene IV: The end.

            [Exeunt]
        """)
        captured = capsys.readouterr()
        assert captured.out == '\ndriht\ndnoces\ntsrif'
        assert captured.err == ''
