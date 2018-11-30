Gone Language Specification
---------------------------

This document serves as a reference to the Gone language which you will
be compiling.

1. Lexical Conventions and Syntax
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each statement is terminated by a semicolon.  For example::

    print 3;
    var a int = 4;

A single-line comment is denoted by ``//``.  For example::

    var a int = 4;    // This is a comment

Multiline comments can be written using ``/* ... */``. For example::

    /* 
    This is a multiline
    comment.
    */

An identifier is a name used to identify variables, constants, and functions.
Identifiers can include letters, numbers, and the underscore (_), but
must always start with a non-numeric character.   Gone follows the same
rules as Python.   The following reserved words may not be used as
an identifier::

    const else extern false func if print return true while var

A numeric literal such as 12345 is intepreted as an integer.  A
numeric literal involving a decimal point or scientific notation such
as 1.2345 or 123e2 is interpreted as a floating point number.  
The literals ``true`` and ``false`` are interpreted as booleans.

A character literal such as `'h'` is interpreted as a single
text character. Escape codes such as ``\'``, ``\n``, ``\\``, and ``\xhh``
are to be interpreted in the usual way as well.

The following operators are recognized::

    +  -  *  /  <  <= > >= == != ! && ||

The following tokens serve as delimiters in expressions, function calls,
and function definitions::

    (  )  , { }

Curly braces are used to enclose blocks of statements. For example::

    if (a < b) {
       statement1;
       statement2;
    } else {
       statement3;
       statement4;
    }

2. Types
~~~~~~~~

There are four built-in datatypes; ``int``, ``float``, ``char``, and
``bool``.

``int`` is a signed 32-bit integer.  ``float`` is a 64-bit double precision
floating point number.  ``char`` is a single character, represented
as a byte. ``bool`` represents the boolean values ``true`` and ``false``.

Variables are always declared with an explicit type and may include
and optional initializer.  For example::

    var a int;
    var b float = 3.14159;
    var c bool;  
    var d char = 'h';

Constants may be declared without a type, in which case the type is
inferred from the value::

    const e = 4;        // Integer constant
    const f = 2.71828;  // Float constant
    const g = true;     // Bool constant
    const h = 'h';      // Char constant

3. Operators and Expressions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

3.1 Numeric operators
^^^^^^^^^^^^^^^^^^^^^

Numeric types support the binary operators ``+``, ``-``, ``*``, and
``/`` with their standard mathematical meaning.  Operators require
both operands to be of the same type.  For example, ``x / y`` is only
legal if ``x`` and ``y`` are the same type.  The result type is always
the same type as the operands.   Note: for integer division, the result
is an integer and is truncated.

Numeric types also support the unary operators of ``+`` and ``-``. For
example::

     z = -y;
     z = x * -y;

No automatic type coercion is performed.  Thus, integers and floats
can not be mixed together in an operator.  If this is desired, one of
the values needs to be explicitly converted to the other using a
conversion function (unspecified) of some kind.

3.2 Character operations
^^^^^^^^^^^^^^^^^^^^^^^^

Character literals support no operations whatever.  A character is simply
a "character" and that's it.

3.3 Relations
^^^^^^^^^^^^^

The operators ``<``, ``<=``, ``>``, ``>=``, ``==``, and ``!=`` can
be used to compare two values and have the standard meaning found in
Python.   The two operands must be of the same type.  

The logical operators ``&&``, ``||``, and ``!`` implement the logical
and, logical-or, and logical negation operations.  These operators only
work on boolean values.   Thus, the following expressions are legal::

     (a < 3) && (a > 0)
     !(a == 0)

Expressions such as the following are illegal unless ``a`` and ``b`` are
of type ``bool``::

     a && b;     // Illegal unless a,b are bools

Although character literals support no mathematical operators, they are
comparable.

3.4 Boolean types and operators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Boolean types only support the operators ``==``, ``!=``, ``&&``,
``||``, and ``!``.  In particular, boolean values are not equivalent
to integers and can not be used in mathematical operators involving
numbers.

3.5 Associativity and precedence rules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All operators are left-associative.   The following chart shows the
precedence rules from highest to lowest precedence::

       +, -, !  (unary)       // Highest precedence
       *, /
       +, -
       <, <=, >, >=, ==, !=
       &&
       ||                     // Lowest precedence

Relational operators may NOT be chained or associate together. For example::

      a < b && b < c;        // OK
      a < b < c;             // Illegal

3.6 Short-circuit evaluation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The logical operators ``&&`` and ``||`` should implement short-circuit behavior
in evaluation.   That is, in the expression ``a && b``, if ``a`` evaluates
to ``false``, then ``b`` is not evaluated.  Similarly, if ``a`` evaluates
to ``true``, then ``a || b`` does not evaluate ``b``.

4. Control Flow
~~~~~~~~~~~~~~~

The ``if`` statement is used for conditions. For example::

    if (a < b) {
       statements;
       ...
    } else {
       statements;
       ...
    }

The conditional expression used to test must evaluate to a ``bool``.
Code such as the following is an error unless ``a`` has type ``bool``::

    if (a) {     // Illegal unless a is type bool
       ...
    }

The ``else`` clause is optional.

The ``while`` statement can be used to execute a loop.  For example::

    while (n < 10) {
        statements;
        ...
    }

This executes the enclosed statements as long as the associated
condition is ``true``.   Again, the conditional expression must
evaluate to type ``bool``.

5. Functions
~~~~~~~~~~~~

Functions can be defined using the ``func`` keyword as follows::

    func fib(n int) int {
        if (n <= 2) {
           return 1;
        } else {
           return fib(n-1) + fib(n-2);
        }
    }

Functions must supply types for the input parameters and return value as shown.

External functions in the C standard library can be declared using
``extern`` as follows::

    extern func sin(x float) float;

These functions must already exist in C or loaded shared libraries
or linkage will fail.

When calling a function, all function arguments are fully evaluated 
prior to making the associated function call.   That is, in a 
call such as ``foo(a,b,c)``, the arguments ``a``, ``b``, and ``c``
are fully evaluated to a value first.

6.  Scoping rules
~~~~~~~~~~~~~~~~~

Declarations are placed into one of two scopes.  Declarations defined
outside of a function are global. Declarations inside a function are
local.   Local declarations are not visible to any other part of a
program except for code in the same function.  Statements inside a
function can access declarations in local or global scope.  For example::

    var a int;     // Global variable

    func foo(b int) int {
        var c int;          // Local variable
        ...
    }

Nested function definitions and closures are not supported.  For 
example::

    func foo(b int) int {
         func bar(c int) int {   // Illegal. Nested functions not allowed
              ...
         }
         ...
    }

7.  Main entry point and initialization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Functions always begin execution in a function ``main()`` which takes
no arguments and returns an integer result.  For example::

    func main() int {
        var i int = 0;
        while (i < N) {
           print fib(i);
           i = i + 1;
        }
        return 0;
    }

Any initialization steps related to global variables must execute
prior to the invocation of ``main()``.   For example::

    var a int = 4;
    var b int = 5;
    var c int = a + b;     // Evaluates prior to main()
    ...
    func main() int {
       ...
    }

8. Printing
~~~~~~~~~~~

The built-in ``print value`` operation can be used for debugging output.
It prints the value of any type given to it. 

