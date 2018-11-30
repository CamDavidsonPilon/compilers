Exercise 3 - Type Checking
--------------------------

**IMPORTANT: It is critical to work this entire exercise before starting Project 3.**

An important role of a compiler is to detect common programming errors
such as undefined identifiers, bad operations, and type errors.  Let's
consider an example with the following Python code::

    a = 23
    b = 42
    c = 'hello'
    d = a + 2*b
    e = a + z
    f = a + c
    g = c * c

This code has three errors in it.  First, the name ``z`` is undefined so
the statement ``e = a + z`` in the fifth line is going to fail.
Second, the statement ``f = a + c`` has a type error in it since
it is trying to add an integer and a string together.  Finally, the
statement ``g = c * c`` has a type error since strings don't support
multiplication.

Python defers all error checking to runtime. So, you wouldn't find out
about these problems until the statements execute.  However,
suppose you wanted to have a compiler check in advance?  Let's see how
to do that.

Parse Tree Walking - The Visitor Pattern
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Start by making a file ``simplecheck.py`` with the following code in it::

    # simplecheck.py
    code = '''
    a = 23
    b = 42
    c = 'hello'
    d = a + 2*b
    e = a + z
    f = a + c
    g = c * c
    '''

    import ast
    top = ast.parse(code)
    print(ast.dump(top))

This code parses a code fragment into an AST which is then printed.
You should get output such as this (reformatted slightly)::

    Module(body=[Assign(targets=[Name(id='a', ctx=Store())], value=Num(n=23)), 
                 Assign(targets=[Name(id='b', ctx=Store())], value=Num(n=42)), 
                 Assign(targets=[Name(id='c', ctx=Store())], value=Str(s='hello')), 
                 Assign(targets=[Name(id='d', ctx=Store())], 
                        value=BinOp(left=Name(id='a', ctx=Load()), op=Add(),
                        right=BinOp(left=Num(n=2), op=Mult(), right=Name(id='b',
                        ctx=Load())))), 
                 Assign(targets=[Name(id='e', ctx=Store())],
                        value=BinOp(left=Name(id='a', ctx=Load()), op=Add(),
                        right=Name(id='z', ctx=Load()))), 
                 Assign(targets=[Name(id='f', ctx=Store())], 
                        value=BinOp(left=Name(id='a', ctx=Load()), op=Add(), 
                        right=Name(id='c', ctx=Load())))
                 Assign(targets=[Name(id='g', ctx=Store())], 
                        value=BinOp(left=Name(id='c', ctx=Load()), op=Mult(), 
                        right=Name(id='c', ctx=Load())))])

This is a bit messy, but within the AST you can see ``Name`` nodes referring to
variable names as well as the context in which they are being used (load or store).  Let's
write a class that prints this out. Add this to your ``simplecheck.py`` file::

    # simplecheck.py
    ...
    class SimpleCheck(ast.NodeVisitor):
        def visit_Name(self,  node):
            print(node.id, node.ctx)

    SimpleCheck().visit(top)

This class is utilizing a technique known as the "visitor pattern."
The idea is relatively simple. There is a base class ``NodeVisitor``
that has a single method ``visit(node)`` which executes a traversal of
the AST.  See the file ``gone/ast.py`` for an implementation (or look
in Python's own ``ast`` module).  To process different kinds of nodes,
you subclass ``NodeVisitor`` and define methods such as
``visit_Name()`` above.  Whenever that node is encountered in walking
the tree, the method will be fired.  If you run the above program,
you'll get output that looks like this::

    a <_ast.Store object at 0x105dd7898>
    b <_ast.Store object at 0x105dd7898>
    c <_ast.Store object at 0x105dd7898>
    d <_ast.Store object at 0x105dd7898>
    a <_ast.Load object at 0x105dd7780>
    b <_ast.Load object at 0x105dd7780>
    e <_ast.Store object at 0x105dd7898>
    a <_ast.Load object at 0x105dd7780>
    z <_ast.Load object at 0x105dd7780>
    f <_ast.Store object at 0x105dd7898>
    a <_ast.Load object at 0x105dd7780>
    c <_ast.Load object at 0x105dd7780>
    g <_ast.Store object at 0x105dd7898>
    c <_ast.Load object at 0x105dd7780>
    c <_ast.Load object at 0x105dd7780>

Carefully study this output and compare it to the sample code.  The variable
name and context should match the usage of that name in the code. 

(b) Symbol Tables
~~~~~~~~~~~~~~~~~

To perform program checking, compilers manage a symbol table.  A
symbol table is a mapping from identifier names to information
about the identifier. Let's try a really simple symbol table example.
In this example, we modify our ``SimpleCheck`` class to record
information about names being stored and loaded.  An error is reported
for all undefined names::

    class SimpleCheck(ast.NodeVisitor):
        def __init__(self):
            self.symbols = set()

        def visit_Name(self, node):
            # If storing, a name is added to the symbol table
            if isinstance(node.ctx, ast.Store):
                self.symbols.add(node.id)

            # If loading, check for definition in symbol table
            elif isinstance(node.ctx, ast.Load):
                if node.id not in self.symbols:
                    print('Error: Name %s not defined' % node.id)

    SimpleCheck().visit(top)

If you run this program, you should get output like this::

    Error: Name z not defined

Good.  You've found one of the errors in the code.

Introducing Types
~~~~~~~~~~~~~~~~~

In most programming languages, values have an associated type. For
example, ``23`` is a number and ``'hello'`` is a string.  The behavior
of various operations then depend on these types.   To build a type
system, the first step is annotating values with type information.
Let's do that.   Modify the the ``SimpleCheck`` class like this::

    class SimpleCheck(ast.NodeVisitor):
        def __init__(self):
            self.symbols = { }

        def visit_Num(self, node):
            node.type = 'num'

        def visit_Str(self, node):
            node.type = 'str'

        def visit_Assign(self, node):
            # Visit the right-hand-side value to get types assignment
            self.visit(node.value)

            # Temporarily store the right-hand-side so it's visible in other methods
            self.assignment_value = node.value

            # Visit each target on the left-hand-side
            for target in node.targets:
                self.visit(target)
            
        def visit_Name(self, node):
            # If storing, a type is added to the symbol table (from self.assignment_value above)
            if isinstance(node.ctx, ast.Store):
                self.symbols[node.id] = getattr(self.assignment_value, 'type', None)

            # If loading, check for definition in symbol table
            elif isinstance(node.ctx, ast.Load):
                if node.id not in self.symbols:
                    print('Error: Name %s not defined' % node.id)

    checker = SimpleCheck()
    checker.visit(top)
    print(checker.symbols)

This class introduces a few new ideas.  First, the symbol table has
been changed to a dictionary. We've done this because we're going to
make a mapping from names to type information. Next, methods have
been added for ``Num`` and ``Str`` nodes.  In these methods, a
``type`` attribute is added to the AST node.  For now, this is set to a
simple type name.  An important thing about these methods is that they
are the entry point for types being used elsewhere (types are associated
with values). 

Next, a new method has been added for the ``Assign`` node.  This
method visits the assigned value first in order to figure out its
type.  The method then sets an attribute (``assignment_value``) to temporarily record the
right-hand-side of the assignment before visiting each of the
assignment targets one-by-one.  The ``visit_Name()`` method is
modified slightly to store the type of the assigned value in the
symbol table.  Note: The whole arrangement of this is tricky. Carefully
study the code and make sure you understand what's happening.

If you run this modified code, you should get output like this::

    Error: Name z not defined
    {'b': 'num', 'e': None, 'd': None, 'c': 'str', 'a': 'num', 'f': None, 'g': None}

As before, you'll get output about the undefined variable ``z``. You'll
also get a dictionary showing known type information for different
variables.   For simple assignments such as ``a = 23``, you'll
see the symbol table recording a type of ``'num'``.  Good, this is
what you want.  For complex assignments such as ``d = a + 2*b``, the
type is set to ``None`` however.  We need to fix that.

Type Propagation
~~~~~~~~~~~~~~~~

To gather more information about types, you need to propagate
information in operations where values are used (e.g., expressions,
etc.).  To do this, add a method ``visit_BinOp()`` and modify
``visit_Name()``.  These methods are now going to attach a ``type``
attribute to their associated AST node::

    class SimpleCheck(ast.NodeVisitor):
        ...
            
        def visit_Name(self, node):
            # If storing, a type is added to the symbol table (from self.assignment_value above)
            if isinstance(node.ctx, ast.Store):
                self.symbols[node.id] = getattr(self.assignment_value, 'type', None)

            # If loading, check definition in symbol table and attach type
            elif isinstance(node.ctx, ast.Load):
                if node.id not in self.symbols:
                    print('Error: Name %s not defined' % node.id)
                else:
                    # Attach known type information to the node (from symbol table)
                    node.type = self.symbols.get(node.id, None)

        def visit_BinOp(self, node):
            self.visit(node.left)
            self.visit(node.right)
            # Propagate the type from the left operand to the result
            node.type = getattr(node.left, 'type', None)

    checker = SimpleCheck()
    checker.visit(top)
    print(checker.symbols)

If you run this program, you'll now get this output::

    Error: Name z not defined
    {'b': 'num', 'e': 'num', 'd': 'num', 'c': 'str', 'a': 'num', 'f': 'num', 'g': 'str'}

Carefully observe that types have propagated to all of the variable names.  We're
still not finding the type error in the assignment to ``f = a + c`` though. Continue.

Type Checking
~~~~~~~~~~~~~

Modify the ``visit_BinOp()`` method so that it looks like this::

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        left_type = getattr(node.left, 'type', None)
        right_type = getattr(node.right, 'type', None)
        if left_type != right_type:
            print('Error: Type error.  %s %s %s' % (left_type, type(node.op).__name__, right_type))
            node.type = 'error'
        else:
            node.type = left_type

In this code, we've added some code to check that the left and right hand sides of a
binary operator are the same type.  If not, an error is indicated.  Run the program
and you should now get this::

    Error: Name z not defined
    Error: Type error.  num Add None
    Error: Type error.  num Add str
    {'d': 'num', 'e': 'error', 'a': 'num', 'b': 'num', 'f': 'error', 'c': 'str', 'g': 'str'}

Excellent.  By the way, the reason you get two type-error messages is that the
expression ``a + z`` is still checked even though ``z`` is an undefined variable
name.  You could probably suppress that error, but for now it's fine.  

Type Capabilities
~~~~~~~~~~~~~~~~~

Our code almost works, but it's still missing one of the type errors.
The statement ``g = c * c`` should fail because strings don't allow
multiplication.  In order to handle this, you need to build some
concept of type capabilities.  For example, the idea that
multiplication works for numbers, but not for strings.  There are
also some oddities in result types. For example, multiplying a string
by a number is allowed and produces a string.

There are MANY ways to structure this, but in the interest of brevity,
let's specify capabilities as a dict of operators, types, and result types.
Try this code::

    # simplecheck.py

    # dict mapping valid type/operator combinations to result types
    supported_binops = {
        ('num', 'Add', 'num') : 'num',
        ('num', 'Mult', 'num') : 'num',
        ('num', 'Sub', 'num') : 'num',
        ('num', 'Div', 'num') : 'num',
        ('string', 'Add', 'string') : 'string',
        ('string', 'Mult', 'num') : 'string',
        ('num', 'Mult', 'string') : 'string'
    }

    class SimpleCheck(ast.NodeVisitor):
        ...

        def visit_BinOp(self, node):
            self.visit(node.left)
            self.visit(node.right)
            left_type = getattr(node.left, 'type', None)
            right_type = getattr(node.right, 'type', None)
            op = type(node.op).__name__
            if (left_type, op, right_type) not in supported_binops:
                print('Error: Type error.  %s %s %s' % (left_type, op, right_type))
                node.type = 'error'
            else:
                node.type = supported_binops[left_type, op, right_type]
         ...

If you run this final code, you'll get this output::

    Error: Name z not defined
    Error: Type error.  num Add None
    Error: Type error.  num Add str
    Error: Type error.  str Mult str
    {'b': 'num', 'g': 'error', 'd': 'num', 'c': 'str', 'e': 'error', 'f': 'error', 'a': 'num'}

Excellent!  You've found all of the type errors.  This is the general idea.

Discussion
~~~~~~~~~~

In your compiler project, you are going to take all of the ideas
discussed in this exercise and apply them to your compiler.
Specifically:

- You'll need to write visitor classes for analyzing the AST and reporting errors.
- You'll need to add a symbol table for recording information about identifiers
- You'll need to figure out some way to describe types.
- You'll need to propagate type information across AST nodes
- You'll need to think about ways to encode type capabilities and other details

One thing to keep in mind is that there is much more to type checking
than presented here.  In some sense, this is just a shell of the idea.
There are potentially other nasty things like automatic type
conversions (e.g., int to float coercion), operations involving mixed
types, and so forth.  For now, let's put some of these concerns on the
backburner.

Proceed to Project 3.
