Project 7 - Control Flow
------------------------

Files Modified::

   Everything

Caution
~~~~~~~

Make sure you fully work through Exericse 7 before starting this
project.

Preliminaries
~~~~~~~~~~~~~

Don't forget to commit and tag your Project 6 code::

     bash % git commit -m "Project 6 complete"
     bash % git tag project6

Once again, this project involves changes to almost every part of the
compiler.   Failure to commit your previous code is not advised.

Overview
~~~~~~~~

In this project, you're going to add basic control-flow constructs to
your compiler.  Specifically, an ``if-else`` statement::

    if relation {
         statements
    } else {
         statements
    }

and a ``while``-loop::

    while relation {
         statements
    }

These statements are to have the familiar semantics you are used to
from other programming languages.

Suggested sequence of work:

1. Add tokens for ``if``, ``else``, and ``while`` to ``gone/tokenizer.py``.

2. Add new AST nodes for a conditional and while-loop to ``gone/ast.py``.

3. Add new parsing rules to ``gone/parser.py``.

4. Add new type-checking code to ``gone/checker.py``.  Your checking code 
   should enforce the requirement that the expression given to ``if`` or ``while``
   evaluates to a boolean value.

5. Modify the file ``gone/ircode.py`` to generate code as a sequence of blocks.
   To do this, add support for block labels and branching instructions
   that connect the labels.

6. Modify the file ``gone/llvmgen.py`` so that it emits an LLVM basic
   block for each block label and it connects the blocks using LLVM
   branch instructions.

Making all of these changes will take some time, but may not involve
as many changes to compiler as you think.    Most of the heavy work is
going to involve the latter stages where you need to extend the code
generator, and LLVM backend to handle the basic block structures.
Take your time and simply work step-by-step through the parts.

Suggestions
~~~~~~~~~~~

Modifying the LLVM generator is not hard, but subtle.  I'd suggest
scanning the instruction sequence for all block labels in advance.
Then, make the LLVM blocks in advance.  For example, do this as a
first step::

    self.blocks = { }
    for instr in ircode:
        if instr[0] == 'BLOCK':
            self.blocks[instr[1]] = self.function.append_basic_block(instr[1])

After you've done this, you'll have a dictionary mapping block labels to
LLVM blocks.  Use this when emit the appropriate branching statements.
For example::

     def emit_branch(self, label):
         self.builder.branch(self.blocks[label])

You'll need to add a few additional parts, but the code is probably
more simple than you think.

Testing
~~~~~~~

The following files are available for testing::

    Tests/cond.g          # A simple conditional
    Tests/nestedcond.g    # Nested conditionals
    Tests/fact.g          # Compute factorials
    Tests/fib.g           # Compute fibonacci numbers
    Tests/nestedwhile.g   # Nested while loops
    Tests/badcontrol.g    # Some error checks

To run the tests, you should just be able to run your compiler::

    bash % python3 -m gone.run Tests/fact.g
    1
    2
    6
    24
    120
    720
    5040
    40320
    362880
    bash %





