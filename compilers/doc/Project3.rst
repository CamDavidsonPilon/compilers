Project 3 - Types and Program Checking
--------------------------------------

Modified files::
 
    gone/checker.py
    gone/typesys.py

Preliminaries
~~~~~~~~~~~~~

Don't forget to commit and tag your Project 2 code::

     bash % git commit -m "Project 2 complete" .
     bash % git tag project2

Overview
~~~~~~~~

In this project, you are going to add a type system and type checking
to your compiler.  This is where your compiler is going to report most
of its error messages for things such as invalid operators, undefined
variable names, and so forth.

Further instructions are found in the files ``checker.py`` and 
``types.py``.

Testing
~~~~~~~

The following tests are available::
   
    Tests/checktest0.g
    Tests/checktest1.g
    Tests/checktest2.g
    Tests/checktest3.g
    Tests/checktest4.g
    Tests/checktest5.g
    Tests/checktest6.g
    Tests/checktest7.g

Information and implementation tips are given in each test file. To
run these tests, use a command such as::

    bash % python3 -m gone.checker Tests/checktest0.g

Commentary
~~~~~~~~~~

Error reporting is a notoriously difficult part of compiler writing.
In writing your checker, it's important to focus on small steps and to
take your time.  The above tests are organized in a way that follows
one possible implementation strategy.

You may find it to be difficult to catch certain kinds of errors.
Keep in mind that even if you don't detect every possible error, you
can still proceed to later stages of the project.  The main downside
is that your compiler might try to do crazy things with incorrect
programs if you allow them to continue on to code generation.



