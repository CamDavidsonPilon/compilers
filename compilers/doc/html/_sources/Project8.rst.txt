Project 8 - Functions
---------------------

Files Modified::

     Everything!

Preliminaries
~~~~~~~~~~~~~

Don't forget to commit and tag your Project 7 code::

     bash % git commit -m "Project 7 complete"
     bash % git tag project7

This next stage of the project is the most difficult of all.   Failure
to commit your previously "working" code is not advised.

Overview
~~~~~~~~

Full disclaimer:  This part of the project is probably the most difficult to
implement and will probably require 3-6 hours of work.  You will need to
make changes to virtually every part of the compiler to do it.

In this project, you are going to give your compiler support for user
defined functions.  For example::

    // Function definition
    func add(x int, y int) int {
         return x+y;
    }

    // Function definition
    func fibonacci(n int) int {
         if n > 1 {
            return fibonacci(n-1) + fibonacci(n-2);     // Return
         } else {
            return 1;    // Return
         }
     }

     const MAXFIB = 20;       // Global

     // Function definition (entry point)    
     func main() int {
          print add(2,3);            // Function call
          var n int;
          while n < MAXFIB {
              print fibonacci(n);    // Function call
          }
          return 0;
     }

Here are the main features that you are going to implement:

1. Function definitions via the ``func`` keyword.
2. The ability to return a value from a function using ``return``.
3. Global and local scoping rules for variables.
4. Calling of main() function as the program entry point

There are many different steps involved.  Here is the order
in which you should probably work on it:

1. Add a new ``return`` token to the lexer.

2. Define some new AST nodes corresponding to a function definition and the
return statement.  You'll probably need to introduce additional AST nodes
for function parameters, parameter lists, arguments, and argument expression lists.
   
3. Add new parsing rules to your parser for all of the new AST nodes.
Specifically, you need to support function definitions and return
statements.

4. Modify the type checking code to use two-level scoping.  For
instance, instead of having just a single symbol table, define a
global symbol table and a local symbol table for use when inside
a function body.  Modify the code that stores symbols to use the
appropriate symbol table depending on content.  Modify the code that
looks up symbols to consult both symbol tables.   You may also want to
store additional information on declarations to indicate whether or
not they are global or local (this will provide to be useful later
during code generation).

5. Add new type checking rules for all of the new AST nodes. This
type checking may include:

   a. Check that function names are defined.
   b. Check that a name corresponds to a function declaration.
   c. Not allowing nested function definitions.
   d. Making sure the number of arguments and types match in function calls.
   e. Making sure the value returned by a function matches the function return type.

6. Extend the SSA intermediate code so that it understands the distinction
between local and global variables.   For example, refine variable allocation
so that there are two different methods::

    ('ALLOCI', name)        # Allocate a local variable
    ('VARI', name)          # Allocate a global variable

You might need to add more instructions later, but these are probably a minimum.

7. Modify code generation so that each function declaration is parsed into
its own set of instruction blocks.  The code generator should collect all of
the resulting code fragments (e.g., you should make a list consisting of
the name of a function, function parameter information, followed by the
list of the instructions making up the function body).
function body).

8. Extend the control-flow analysis code to detect functions that
end without some kind of return statement (i.e., functions that
just fall off the end).  (optional)

9. Have the code generator collect code that doesn't belong in any
proper function definition and put it into a special initialization
function.  This step is needed to handle things such as the
initialization of global variable values.

10. Modify the LLVM code generator to emit code for all of the
functions that are defined. 
   
General Advice
~~~~~~~~~~~~~~

Success with this part of the project requires careful and methodical work. 
Don't worry about rushing through everything.  Just take it one step at a time.
Test things as you go. For a long time it will seem like you aren't making
any progress, but then it will just suddenly come together at the end.

Testing
~~~~~~~

The following files are available::

     Tests/func.g                # Some simple functions
     Tests/funcerrors.g          # Common errors involving functions
     Tests/funcret.g             # Tests for missing return statements

Real Programs
~~~~~~~~~~~~~

The ``Programs/`` directory has a collection of Gone programs that
you can try with your final compiler.  For example, making a Mandelbrot
set::

     bash % python3 -m gone.run Programs/mandel.g
     ... look at the output ...


