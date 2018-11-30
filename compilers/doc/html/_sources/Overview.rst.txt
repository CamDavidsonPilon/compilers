Compiler Project Overview
-------------------------

You are going to be implementing the core of a simple programming
language called "gone."  Gone supports the following features:

- Evaluation of expressions (math)
- Integers, floats, characters, and bools.
- Assignment to variables
- Printing
- Basic control flow (if, while)
- User-defined functions

Although the language is simple, you are going to have to write all of
the core components of an actual compiler, including all of the
parsing, type checking, control-flow analysis, intermediate code
generation, and output code.

The implementation approach is going to be incremental.  The first
five projects are going to take you through all of the core stages of
compilation of lexing, parsing, type checking, and code generation for
a small subset of the language.  The last three projects involve
expanding your compiler to include more advanced features.

Ultimately, the final output of your compiler will be LLVM
intermediate representation from which you will be able to compile and
run real programs.  However, much of the compiler design will be quite
general and suitable for doing other things such as writing an
interpreter.

A Taste of Gone
~~~~~~~~~~~~~~~

Here is a sample of a simple Gone program that computes the ever-so-useful
Fibonacci numbers::

    /* fib.g -  Compute fibonacci numbers */

    const LAST = 30;            // A constant declaration

    // A function declaration
    func fibonacci(n int) int {
         if n > 1 {              // Conditionals
            return fibonacci(n-1) + fibonacci(n-2);
         } else {
            return 1;
         }
     }

     func main() int {
         var n int = 0;           // Variable declaration
	 while n < LAST {         // Looping (while)
	    print fibonacci(n);   // Printing
            n = n + 1;            // Assignment
         }
	 return 0;
     }

The ``fib.g`` program above can be found in the directory
``Programs/fib.g``.

Running and Compiling Programs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``gone`` project allows programs to be compiled and executed
in three different ways.  First, you can compile a program to
intermediate code and have it run inside an interpreter::

    bash % python3 -m gone.interp Programs/fib.g
    1
    1
    2
    3
    5
    8
    13
    21
    34
    55
    ...
    bash %

You should see output similar to the above being generated, albeit
very slowly.  This is the most portable technique for running Gone
code as it involves nothing but pure Python code.

The ``fib.g`` program can also be compiled to a stand-alone executable::

    bash % python3 -m gone.compile Programs/fib.g
    bash % ./a.out
    1
    1
    2
    3
    5
    ...
    bash %

This creates a program called ``a.out``.  If you run it, you should
see the same output as the interpreter, but substantially faster. This
is executing native machine code on your system.  Creating this
executable requires the ``clang`` C/C++ compiler.  If you don't have
it installed correctly, compilation will probably fail.

If you don't have ``clang`` installed, you can also run the program as
a just-in-time compiled binary inside Python. To do this, you first need
to build a run-time library::

    bash % cd gone
    bash % make mac    #  Change to make linux on Linux

Next, you can try running the program::

    bash % cd ..
    bash % python3 -m gone.run Programs/fib.g
    bash % ./a.out
    1
    1
    2
    3
    5
    ...
    bash %

This should produce the same output as before at native speed.  This version
is using LLVM to generate native machine code, but not does have a dependency
on ``clang.``

Reference Implementation
~~~~~~~~~~~~~~~~~~~~~~~~

The ``goner`` directory contains a reference implementation for the
first part of the project that you can use for testing, hints, and
comparing against your own code.  It's okay to look at this code as
you work, but to get the most out of the project, you should work to
make your own solution.

As an aside, the reference implementation is a bare-bones implementation.
You should think of various ways to make your compiler and more featureful.

Language Reference
~~~~~~~~~~~~~~~~~~

The ``Gone.rst`` file contains an official specification for the language.

