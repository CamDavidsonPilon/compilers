Project 1 - Lexing
------------------

Files Modified::

    gone/errors.py
    gone/tokenizer.py

Preliminaries
~~~~~~~~~~~~~

All of your work on the compiler is going to take place in a directory
``gone``.  In that directory, you will already find a set of files
corresponding to different parts of the compiler project.  Each 
file has further directions about how to proceed. 

It is strongly advised that you put your work under version control
using what tool you're comfortable using.  For example with Git::

    bash % cd compilers
    bash % git init
    bash % git add gone/*
    bash % git commit -m "Project start" .
    bash %

For the remainder of the project, it is strongly advised that you work
with all files under version control and commit changes after every
major project stage.  Should you break something in a later project,
this will make it easier to go back.

Your Task
~~~~~~~~~

The first part of the compilers project involving a lexer for a subset
of the Gone language involving expressions.  Go to the file
``tokenizer.py`` and follow the instructions contained within.

Testing
~~~~~~~

The following files can be used for testing the input to your lexer::

     Tests/lextest0.g
     Tests/lextest1.g
     Tests/lextest2.g
     Tests/lextest3.g
     Tests/lextest4.g
     Tests/lextest5.g

You should run the tests by typing::

     bash % python3 -m gone.tokenizer filename
     ... get output ...
     bash %

If you need to compare your output against the reference compiler,
use::

    bash % python3 -m goner.tokenizer filename


