Exercise 1  - Lexing
--------------------

Note: Solution code to this exercise is found in ``Exercises/Solutions/1``.
Look at it if you get stuck.

The first step of writing a compiler is to write a lexer or tokenizer.
The role of a lexer is to identify valid symbols in an input text.
For example, if you had text like this::

         a = 3 + (4 * 5)

It is broken down into a series of tokens like this::

         ID(a) '=' NUMBER(3) '+' '(' NUMBER(4) '*' NUMBER(5) ')'

To perform lexing, each token is identified by a regular expression.
Thus, you can use features of Python's ``re`` module to do it.

Manual tokenizing using re
~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's start by seeing how to manually tokenize text using the ``re``
module.  Make a file called ``ex1.py`` and define the following code::

    # ex1.py

    import re

    ID = r'(?P<ID>[a-zA-Z_][a-zA-Z0-9_]*)'
    NUMBER = r'(?P<NUMBER>\d+)'
    SPACE = r'(?P<SPACE>\s+)'

    patterns = [ID, NUMBER, SPACE]

    # Make the master regex pattern
    pat = re.compile('|'.join(patterns))

    def tokenize(text):
        index = 0
        while index < len(text):
            m = pat.match(text,index)
            if m:
                yield (m.lastgroup, m.group())
                index = m.end()
            else:
                raise SyntaxError('Bad char %r' % text[index])

    # Sample usage
    text = 'abc 123 cde 456'

    for tok in tokenize(text):
        print(tok)

In this code, there are three regular expressions that have been
combined into a master pattern.  The ``tokenize()`` function breaks
the text apart and yields tuples.  Run the code.  You should see
output like this::

    ('ID', 'abc')
    ('SPACE', ' ')
    ('NUMBER', '123')
    ('SPACE', ' ')
    ('ID', 'cde')
    ('SPACE', ' ')
    ('NUMBER', '456')

Ignored Characters
~~~~~~~~~~~~~~~~~~

When tokenizing, there is often text you want to ignore such as whitespace.
Modify the ``ex1.py`` program above so that the ``SPACE`` token is ignored.
When you run the program, you should now get the following tokens::

    ('ID', 'abc')
    ('NUMBER', '123')
    ('ID', 'cde')
    ('NUMBER', '456')

Bad Characters
~~~~~~~~~~~~~~

Change the text in the previous example to the following::

    text = 'abc 123 $ cde 456'

Run the program again.  You should see output like this::

    ('ID', 'abc')
    ('NUMBER', '123')
    Traceback (most recent call last):
      File "ex1.py", line 29, in <module>
       for tok in tokenize(text):
      File "ex1.py", line 25, in tokenize
        raise SyntaxError('Bad char %r' % text[index])
    SyntaxError: Bad char '$'

Modify the program so that instead of raising a ``SyntaxError`` the
``tokenize()`` function prints a warning message and continues
tokenizing.  The output should now be like this::

    ('ID', 'abc')
    ('NUMBER', '123')
    Bad character '$'
    ('ID', 'cde')
    ('NUMBER', '456')

To make this change, change the code that raises a ``SyntaxError`` so that
prints a warning message and increments the ``index`` counter to skip the
bad character.

Using a Lexing Tool - Introducing SLY
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The problem of tokenizing text is largely a solved problem.  There is
no need to manually do it as shown.  The SLY tool
(https://github.com/dabeaz/sly) is one such tool for doing this.  Make
a file ``simplelex.py`` and put this code into it::

    # simplelex.py

    from sly import Lexer

    class SimpleLexer(Lexer):
        # Token names
        tokens = { NUMBER, ID }

        # Ignored characters
        ignore = ' \t'

        # Token regexs
        NUMBER = r'\d+'
        ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    
        def error(self, t):
            print('Bad character %r' % t.value[0])
            self.index += 1

    # Example
    if __name__ == '__main__':
        text = 'abc 123 $ cde 456'
        lexer = SimpleLexer()
        for tok in lexer.tokenize(text):
            print(tok)

Run this program.  You should see output like this::

    Token(type='ID', value='abc', lineno=1, index=0)
    Token(type='NUMBER', value='123', lineno=1, index=4)
    Bad character '$'
    Token(type='ID', value='cde', lineno=1, index=10)
    Token(type='NUMBER', value='456', lineno=1, index=14)

With SLY, lexers are defined as class.  The body of the class is
a kind of domain-specific language where you specify the tokens
you want using regular expressions.

A more complete lexer
~~~~~~~~~~~~~~~~~~~~~

Change the last part of the ``simplelex.py`` so that it tokenizes a more
complicated string ``'a = 3 + (4 * 5)'`` like this::

    # simplelex.py
    ...
    # Example
    if __name__ == '__main__':
        text = 'a = 3 + (4 * 5)'
        lexer = SimpleLexer()
        for tok in lexer.tokenize(text):
            print(tok)

Add additional token specifications to the ``SimpleLexer`` class so that
you get the following output::

    Token(type='ID', value='a', lineno=1, index=0)
    Token(type='ASSIGN', value='=', lineno=1, index=2)
    Token(type='NUMBER', value='3', lineno=1, index=4)
    Token(type='PLUS', value='+', lineno=1, index=6)
    Token(type='LPAREN', value='(', lineno=1, index=8)
    Token(type='NUMBER', value='4', lineno=1, index=9)
    Token(type='TIMES', value='*', lineno=1, index=11)
    Token(type='NUMBER', value='5', lineno=1, index=13)
    Token(type='RPAREN', value=')', lineno=1, index=14)

To do this, you should add new token names to the ``tokens`` set and
define regular expressions for each token.

More complicated tokens
~~~~~~~~~~~~~~~~~~~~~~~

Change ``simplelex.py`` so that you can parse different relations
such as ``<``, ``<=``, ``>``, ``>=``, ``==``, and ``!=``.  Make the
test code like this::

    if __name__ == '__main__':
        text = '''
               a < b
               a <= b
               a > b
               a >= b
               a == b
               a != b
        '''
        lexer = SimpleLexer()
        for tok in lexer.tokenize(text):
            print(tok)

The output should look like this::

    Bad character '\n'
    Token(type='ID', value='a', lineno=1, index=12)
    Token(type='LT', value='<', lineno=1, index=14)
    Token(type='ID', value='b', lineno=1, index=16)
    Bad character '\n'
    Token(type='ID', value='a', lineno=1, index=29)
    Token(type='LE', value='<=', lineno=1, index=31)
    Token(type='ID', value='b', lineno=1, index=34)
    Bad character '\n'
    Token(type='ID', value='a', lineno=1, index=47)
    Token(type='GT', value='>', lineno=1, index=49)
    Token(type='ID', value='b', lineno=1, index=51)
    Bad character '\n'
    Token(type='ID', value='a', lineno=1, index=64)
    Token(type='GE', value='>=', lineno=1, index=66)
    Token(type='ID', value='b', lineno=1, index=69)
    Bad character '\n'
    Token(type='ID', value='a', lineno=1, index=82)
    Token(type='EQ', value='==', lineno=1, index=84)
    Token(type='ID', value='b', lineno=1, index=87)
    Bad character '\n'
    Token(type='ID', value='a', lineno=1, index=100)
    Token(type='NE', value='!=', lineno=1, index=102)
    Token(type='ID', value='b', lineno=1, index=105)
    Bad character '\n'

Pay very careful attention to the operator tokens and make sure they
match up.  The token ``<`` needs to go with ``LT`` and ``<=`` needs to
go with ``LE``.  There are some tricky details to worry about here.

You will get error messages about newline characters.  Ignore
those for the moment, we'll fix that shortly.

Newline Tracking
~~~~~~~~~~~~~~~~

Add the following method to your ``SimpleLexer()`` class::


    class SimpleLexer(Lexer):
        ...
        @_(r'\n+')
        def ignore_newline(self,  t):
            self.lineno += t.value.count('\n')
        ...

Rerun the last test.  The error messages should go away and you
should see tokens with properly set line numbers::

    Token(type='ID', value='a', lineno=2, index=12)
    Token(type='LT', value='<', lineno=2, index=14)
    Token(type='ID', value='b', lineno=2, index=16)
    Token(type='ID', value='a', lineno=3, index=29)
    Token(type='LE', value='<=', lineno=3, index=31)
    Token(type='ID', value='b', lineno=3, index=34)
    Token(type='ID', value='a', lineno=4, index=47)
    Token(type='GT', value='>', lineno=4, index=49)
    Token(type='ID', value='b', lineno=4, index=51)
    Token(type='ID', value='a', lineno=5, index=64)
    Token(type='GE', value='>=', lineno=5, index=66)
    Token(type='ID', value='b', lineno=5, index=69)
    Token(type='ID', value='a', lineno=6, index=82)
    Token(type='EQ', value='==', lineno=6, index=84)
    Token(type='ID', value='b', lineno=6, index=87)
    Token(type='ID', value='a', lineno=7, index=100)
    Token(type='NE', value='!=', lineno=7, index=102)
    Token(type='ID', value='b', lineno=7, index=105)

You'll want proper line numbers set when you start to emit
errors and other diagnostic messages.

Identifiers versus Reserved Words
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Programming languages often have reserved keywords like ``if``,
``while``, ``else``, and so forth.  Usually these special words are
handled as a special case of identifiers.  SLY can remap certain
strings to new tokens if you write rules like this::

    class SimpleLexer(Lexer):
        tokens = { ..., ID, IF, ELSE, WHILE, ... }
        ... 
        ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
        ID['if'] = IF
        ID['else'] = ELSE
        ID['while'] = WHILE
        ...

In this code, the ``ID`` rule matches any identifier.  However,
if the identifier exactly matches the special cases for ``if``, 
``else``, or ``while``, the token type is changed as appropriate.

Modify the last part of the program to include these keywords like this::


    if __name__ == '__main__':
        text = '''
               if a < b
               else a <= b
               while a > b
               a >= b
               a == b
               a != b
        '''
        lexer = SimpleLexer()
        for tok in lexer.tokenize(text):
            print(tok)

When you run your program, you should see output like this::

    Token(type='IF', value='if', lineno=2, index=12)
    Token(type='ID', value='a', lineno=2, index=15)
    Token(type='LT', value='<', lineno=2, index=17)
    Token(type='ID', value='b', lineno=2, index=19)
    Token(type='ELSE', value='else', lineno=3, index=33)
    Token(type='ID', value='a', lineno=3, index=38)
    Token(type='LE', value='<=', lineno=3, index=40)
    Token(type='ID', value='b', lineno=3, index=43)
    Token(type='WHILE', value='while', lineno=4, index=56)
    Token(type='ID', value='a', lineno=4, index=62)
    Token(type='GT', value='>', lineno=4, index=64)
    Token(type='ID', value='b', lineno=4, index=66)
    Token(type='ID', value='a', lineno=5, index=79)
    Token(type='GE', value='>=', lineno=5, index=81)
    Token(type='ID', value='b', lineno=5, index=84)
    Token(type='ID', value='a', lineno=6, index=97)
    Token(type='EQ', value='==', lineno=6, index=99)
    Token(type='ID', value='b', lineno=6, index=102)
    Token(type='ID', value='a', lineno=7, index=115)
    Token(type='NE', value='!=', lineno=7, index=117)
    Token(type='ID', value='b', lineno=7, index=120)

Discussion
~~~~~~~~~~

Using the basic machinery of this exercise, you can build simple
tokenizers. Although you can always code a tokenizer by hand, you're
usually better off using a tool like SLY, PyParsing, PLY, etc.
You're now ready to move on to Project 1.







