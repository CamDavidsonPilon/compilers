Exercise 6 - Relations and Booleans
-----------------------------------

This exercise is just an overview of concepts.  Very little
programming is involved.  Just read and work a few examples.

Basic Relations
~~~~~~~~~~~~~~~

Programming languages have operations for relations.  For example::

     a < b
     a <= b
     a > b
     a >= b
     a == b
     a != b

Relations are different than many other binary operators in that the
result type is a boolean, not the same as the operands.  For example::

    >>> a = 2
    >>> b = 3
    >>> a < b
    True
    >>> a > b
    False
    >>>

For booleans, there are additional logical operations for ``and``,
``or``, and ``not``::

    >>> a < b and a > 0
    True
    >>> a > b or a < 0
    False
    >>> not a < b
    False
    >>>

Precedence Rules
~~~~~~~~~~~~~~~~

Relations have lower precedence than other math operators.  For example::

    >>> 1 + 4 < 3 + 5
    True
    >>>
    
Evaluates as::

    >>> (1 + 4) < (3 + 5)
    True
    >>>

Boolean operators ``and`` and ``or`` have lower precedence than relations::

    >>> 2 < 3 and 0 < 1
    True
    >>>

Evaluates as::

    >>> (2 < 3) and (0 < 1)
    True
    >>>

Python allows comparison operators to be chained together::

    >>> 2 < 3 < 0
    False
    >>> 2 < 3 > 0
    True
    >>> 2 < 3 > 0 < 10 > -1
    True
    >>>

Chaining is the same as this::

    >>> 2 < 3 and 3 < 0
    False
    >>> 2 < 3 and 3 > 0
    True
    >>> 2 < 3 and 3 > 0 and 0 < 10 and 10 > -1
    True

Syntactically, it's a little weird to write things such as ``x < y > z``.  
In fact, most programming languages don't permit it.  So, this
is something you might want to disallow in your programming language.
That is, the relations can only be used to compare two values.

Relations in LLVM
~~~~~~~~~~~~~~~~~

Take a look at the program ``cmp.py`` which shows an example of
carrying out a simple relation in LLVM.

Now that you've got the basic idea, proceed to Project 6 and add
relations and booleans to your compiler project.




