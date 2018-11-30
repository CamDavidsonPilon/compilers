Project 5 - LLVM Code Generation
--------------------------------

Files Modified::

     gone/llvmgen.py
     gone/run.py
     gone/compile.py
     gone/gonert.c
     gone/Makefile

Preliminaries
~~~~~~~~~~~~~

Don't forget to commit and tag your Project 4 code::

     bash % git commit -m "Project 4 complete"
     bash % git tag project4

Overview
~~~~~~~~

In this project, you'll going to translate the intermediate SSA code
of your compiler to an LLVM function that you can execute.  

First, go to the file ``gone/llvmgen.py`` and follow the instructions inside for
information on how to make LLVM low-level code.   You should be able to run
your code on the same tests for IRCode::

     Tests/irtest0.g
     Tests/irtest1.g
     Tests/irtest2.g
     Tests/irtest3.g
     Tests/irtest4.g

To run a test and see the LLVM output, use::

     bash % python3 -m gone.llvmgen Tests/irtest0.g

Once you're satisfied that it's working, build the Gone runtime support library::

     bash % cd gone
     bash % make

Once you've done that, you might be able to actually run the code.  You can try 
a command like this::

     bash % python3 -m gone.compile Tests/irtest0.g
     bash % ./a.out
     3
     3.5
     abash %

If compilation doesn't work (might be dicey on your machine), you can alternatively
try running the code using an LLVM JIT compiler::

     bash % python3 -m gone.run Tests/irtest0.g
     3
     3.5
     abash %

Note: The ``compile.py`` and ``run.py`` programs might not require any 
modifications at all.  However, there are some platform dependencies so
some tweaking might be required.

Testing
~~~~~~~

There are several tests in the ``Tests/`` directory that you can find.
For integer operations, you can try::

     bash % python3 -m gone.run Tests/inttest.g
     6
     3
     -1
     12
     3
     1
     -1
     13
     bash %

For floats, try::

     bash % python3 -m gone.run Tests/floattest.g
     6.000000
     3.000000
     -1.000000
     12.000000
     3.000000
     1.000000
     -1.000000
     13.000000
     bash %

For characters, try::

     bash % python3 -m gone.run Tests/chartest.g
     hello
     world
     bash %

A Moment of Zen
---------------

Congratulations!  If you made it this far, you have the end-to-end
processing pipeline of the compiler implemented.  You can compile
basic statements and have them execute.  

Take a few moments to contemplate what you've done, check your code
into version control, and then proceed onto Project 6.





     

