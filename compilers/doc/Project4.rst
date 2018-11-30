Project 4 - Code Generation
---------------------------

Added files::
 
    gone/ircode.py

Preliminaries
~~~~~~~~~~~~~

Don't forget to commit and tag your Project 3 code::

     bash % git commit -m "Project 3 complete"
     bash % git tag project3

Overview
~~~~~~~~

In this part of the project, you are going to make your compiler
generate intermediate instruction code in the form of single static
assignment (SSA).  The output of your compiler will be a sequence of
tuples that look a lot like an abstract machine code. Further
instructions are found in the file ``gone/ircode.py``.

Testing
~~~~~~~

There are a series of test files::

    Tests/irtest0.g
    Tests/irtest1.g
    Tests/irtest2.g
    Tests/irtest3.g
    Tests/irtest4.g

To run these tests, use a command such as::

    bash % python3 -m gone.ircode Tests/irtest0.g

Each test file contains some implementation hints and expected output.
When you're done, you can also try your compiler on the following files::

    Tests/inttest.g
    Tests/floattest.g
    Tests/chartest.g

These tests run the compiler through all of the basic operations on
the different datatypes.



