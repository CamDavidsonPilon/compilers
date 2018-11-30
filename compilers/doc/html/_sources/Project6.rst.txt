Project 6 - Booleans and Relations
----------------------------------

Files Modified::

     Everything!

Preliminaries
~~~~~~~~~~~~~

Don't forget to commit and tag your Project 5 code::

     bash % git commit -m "Project 5 complete"
     bash % git tag project5

Be advised that this project involves changes to almost everything
that you have written before.   Failure to commit your previous
(hopefully working) code before beginning is a sure path to sorrow.

Overview
~~~~~~~~

This project is simple to describe, but a bit of work to implement.  You need
to give your compiler support for boolean operators and relations.
Specifically, you need to add support for the following operators::

    a < b            
    a <= b
    a > b
    a >= b
    a == b
    a != b

    a && b            // Logical and
    a || b            // Logical or
    !a                // Logical negation

You also need to give your compile a proper bool data type along with
``true`` and ``false`` literals.  For example::

     var a bool = true;
     var b bool = false;

All relations and logical operators always produce a result type of
``bool``.  This is a little different than the normal binary operators
where the result is the same type as the operands.

With relations, you get more precedence rules.  Here is the precedence
of operators, from lowest to highest::

    ||
    &&
    <, <=, >, >=, ==, !=
    +, -
    *, /
    Unary : +, -, !

Your compiler should not allow chained relations. For example::

    a < b              // OK
    a < b < c          // Error

See http://www.dabeaz.com/ply/ply.html#ply_nn27 for information on
how to restrict this in the parser by adding 'nonassoc' entries
to the precedence table.

The logical-and, logical-or, and logical negation operators always
expect the operands to be of type bool.  Thus, you will need to
account for things like this::

    var a int = 3;
    var b int = 4;

    var c bool = (a != 0) || (b != 0);      // OK
    var d bool = a || b;                    // ERROR

Implementation Suggestion
~~~~~~~~~~~~~~~~~~~~~~~~~

The relational operators can be added as new binary operators
in your parser.  This may not require much work, but you'll 
need to add some new precedence rules.   Also, the type system
needs to make that all such operations return a result type of
'bool'.

The logical negation operator can be handled as a standard unary
operator.  Just make sure that it only works if the operand is a
boolean type.

Suggested work sequence:

    - Add new tokens to ``gone/tokenizer.py``
    - Add new parsing rules to ``gone/parser.py``
    - Add new fields to types in ``gone/typesys.py`` for relational operators.
    - Add a new boolean type in ``gone/typesys.py``
    - Make sure relations type-check properly in ``gone/checker.py``
    - Add new opcodes for comparisons to ``gone/ircode.py``.
    - Add new code generation rules for LLVM in ``gone/llvmgen.py``.  Add 
      runtime support to ``gonert.c`` if necessary.

Note: You should not have to make major changes (if any) to the code
you already wrote-- all of the above steps involving adding new code,
not rewriting what you did earlier.

Note: This part of the project will probably take a few hours. Take it
easy and just work step by step.

IR Code Generation
~~~~~~~~~~~~~~~~~~

The IR code specification doesn't provide for bools.  Instead, booleans
are represented using integers 0 and 1.   When generating the IR for
relations and other operations, use integer operations.

LLVM Code Generation
~~~~~~~~~~~~~~~~~~~~

To perform comparisons in LLVM, you need to the ``icmp_signed`` and
``fcmp_ordered`` methods of the builder.  Here is a guide of how to do
numeric comparisons in LLVM::

    Integer compares:
    -----------------
    builder.icmp_signed('<', left, right, target)   # left < right
    builder.icmp_signed('<=', left, right, target)   # left <= right
    builder.icmp_signed('>', left, right, target)   # left > right
    builder.icmp_signed('>=', left, right, target)   # left >= right
    builder.icmp_signed('==', left, right, target)    # left == right
    builder.icmp_signed('!=', left, right, target)    # left != right

    Float compares:
    -----------------
    builder.fcmp_ordered('<', left, right, target)   # left < right
    builder.fcmp_ordered('<=', left, right, target)   # left <= right
    builder.fcmp_ordered('>', left, right, target)   # left > right
    builder.fcmp_ordered('>=', left, right, target)   # left >= right
    builder.fcmp_ordered('==', left, right, target)   # left == right
    builder.fcmp_ordered('!=', left, right, target)   # left != right

All of the above operations return a boolean type ``IntType(1)``. 
Depending on how you are doing things, you might need to take the result
and extend it to a 32-bit integer so that it is compatible with other types.
Use this::

    builder.zext(value, IntType(32), target)     # Zero-extend value to a new type

If you ever need to take an integer and truncate it down to a bool, you can
use this::

    builder.trunc(value, IntType(1), target)     # Truncate an int to a bool

There are a few other instructions you'll also need for boolean
expressions::

    builder.and_(left, right, target)             # left && right
    builder.or_(left, right, target)              # left || right

Testing
~~~~~~~

The following files can be used to test your relational and boolean operators::

     Tests/testrel_int.g
     Tests/testrel_float.g
     Tests/testrel_char.g
     Tests/testrel_bad.g

