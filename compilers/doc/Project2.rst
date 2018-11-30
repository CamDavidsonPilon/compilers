Project 2 - Parsing
-------------------

Modified files::

     gone/parser.py
     gone/ast.py

Preliminaries
~~~~~~~~~~~~~

Tag your work on Project 1 in version control.  For example::

    bash % git commit -m "project1 completion" .
    bash % git tag project1

Your task
~~~~~~~~~

In this part of the project, you are going to write a parser and construct
abstract syntax trees (ASTs).  There are two different files you need to
work with.  ``parser.py`` has code for parsing and ``ast.py`` contains
definitions of AST nodes.   Go to each file and follow the instructions
contained therein.

Tip
~~~

It's important to work on this project in small pieces.  You are
strongly advised to try things with small code samples and
progressively build up features as you go.

Testing
~~~~~~~

The Tests/ directory has a series of tests that you can use as you go
along.  Try to work through the files Tests/parsetest0.g,
Tests/parsetest1.g, Tests/parsetest2.g in order as you go.

Run the parser like this::

    bash % python3 -m gone.parser Tests/parsetest0.g
    ... look at the output ...

