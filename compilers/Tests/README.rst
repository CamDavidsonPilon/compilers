Testing Guide
=============

Project1:  Lexing
-----------------
python3 -m gone.tokenizer Tests/testlex1.g       # Tests valid tokens
python3 -m gone.tokenizer Tests/testlex2.g       # Tests bad input

Project2: Parsing
-----------------
There are a series of tests that progressively build up more and more
advanced parts of the language. Work them in order.  Each test file
has a description of what is required along with some hints::

python3 -m gone.parser Tests/parsetest0.g      
python3 -m gone.parser Tests/parsetest1.g
python3 -m gone.parser Tests/parsetest2.g
python3 -m gone.parser Tests/parsetest3.g
python3 -m gone.parser Tests/parsetest4.g
python3 -m gone.parser Tests/parsetest5.g
python3 -m gone.parser Tests/parsetest6.g
python3 -m gone.parser Tests/parsetest7.g

Project 3: Type Checking
------------------------
This part of the project focuses on adding error checks and
validation to your compiler.  It's potentially quite tricky.
Work through each test methodically. Details are given in each
test file::

python3 -m gone.checker Tests/checktest0.g
python3 -m gone.checker Tests/checktest1.g
python3 -m gone.checker Tests/checktest2.g
python3 -m gone.checker Tests/checktest3.g
python3 -m gone.checker Tests/checktest4.g
python3 -m gone.checker Tests/checktest5.g
python3 -m gone.checker Tests/checktest6.g
python3 -m gone.checker Tests/checktest7.g

In order to proceed to Project 4, it is critical that your type
checking code properly propagate datatypes.

Project 4: Intermediate Code
----------------------------
Try running the following tests to test basic code generation.
For each of these tests, you will need to visually compare
expected output with the output of your compiler.  Each test
file has a sample of the output:

python3 -m gone.ircode Tests/irtest0.g
python3 -m gone.ircode Tests/irtest1.g
python3 -m gone.ircode Tests/irtest2.g
python3 -m gone.ircode Tests/irtest3.g
python3 -m gone.ircode Tests/irtest4.g

Project 5: LLVM Code Generation
-------------------------------
The same tests as Project 4 should run.

python3 -m gone.llvmgen Tests/irtest0.g
python3 -m gone.llvmgen Tests/irtest1.g
python3 -m gone.llvmgen Tests/irtest2.g
python3 -m gone.llvmgen Tests/irtest3.g
python3 -m gone.llvmgen Tests/irtest4.g

In addition, there are these two basic tests of integers and floats

python3 -m gone.llvmgen Tests/inttest.g
python3 -m gone.llvmgen Tests/floattest.g

You should be able to compile this code.  Run a.out after each
command::

python3 -m gone.compile Tests/inttest.g
python3 -m gone.compile Tests/floattest.g

You can also try running the code in a JIT::

python3 -m gone.run Tests/inttest.g
python3 -m gone.run Tests/floattest.g

Project 6 : Comparisons and Boolean Operators
---------------------------------------------
Run the following tests on comparison operators::

python3 -m gone.run Tests/testrel_int.g
python3 -m gone.run Tests/testrel_float.g

Note: You might need to run other kinds of more preliminary tests
during development.

The following tests checks some bad comparisons:

python3 -m gone.run Tests/testrel_bad.g

Project 7: Control Flow
-----------------------
The following test files involve control flow features::

python3 -m gone.run Tests/cond.g
python3 -m gone.run Tests/nestedcond.g
python3 -m gone.run Tests/fact.g
python3 -m gone.run Tests/fib.g
python3 -m gone.run Tests/nestedwhile.g

This tests some bad control flow::

python3 -m gone.run Tests/badcontrol.g

Project 8: Functions
--------------------

python3 -m gone.run Tests/func.g
python3 -m gone.run Tests/funcret.g    # Errors involving return statements
python3 -m gone.run Tests/funcerrors.g # Various function related errors
python3 -m gone.run Tests/mandel.g     # Mandelbrot set

For project 8, you can also start running code in the Programs/ directoy.

