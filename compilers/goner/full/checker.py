# gone/checker.py
'''
*** Do not start this project until you have fully completed Exercise 3. ***

Overview
--------
In this project you need to perform semantic checks on your program.
This problem is multifaceted and complicated.  To make it somewhat
less brain exploding, you need to take it slow and in small parts.
The basic gist of what you need to do is as follows:

1.  Names and symbols:

    All identifiers must be defined before they are used.  This
    includes variables, constants, and typenames.  For example, this
    kind of code generates an error:

       a = 3;              // Error. 'a' not defined.
       var a int;

2.  Types of literals and constants

    All literal symbols are implicitly typed and must be assigned a
    type of "int", "float", or "char".  This type is used to set
    the type of constants.  For example:

       const a = 42;         // Type "int"
       const b = 4.2;        // Type "float"
       const c = 'a';        // Type "char""

3.  Operator type checking

    Binary operators only operate on operands of a compatible type.
    Otherwise, you get a type error.  For example:

        var a int = 2;
        var b float = 3.14;

        var c int = a + 3;    // OK
        var d int = a + b;    // Error.  int + float
        var e int = b + 4.5;  // Error.  int = float

    In addition, you need to make sure that only supported 
    operators are allowed.  For example:

        var a char = 'a';        // OK
        var b char = 'a' + 'b';  // Error (unsupported op +)

4.  Assignment.

    The left and right hand sides of an assignment operation must be
    declared as the same type.

        var a int;
        a = 4 + 5;     // OK
        a = 4.5;       // Error. int = float

    Values can only be assigned to variable declarations, not
    to constants.

        var a int;
        const b = 42;

        a = 37;        // OK
        b = 37;        // Error. b is const

Implementation Strategy:
------------------------
You're going to use the NodeVisitor class defined in gone/ast.py to
walk the parse tree.   You will be defining various methods for
different AST node types.  For example, if you have a node BinOp,
you'll write a method like this:

      def visit_BinOp(self, node):
          ...

To start, make each method simply print out a message:

      def visit_BinOp(self, node):
          print('visit_BinOp:', node)
          self.visit(node.left)
          self.visit(node.right)

This will at least tell you that the method is firing.  Try some
simple code examples and make sure that all of your methods
are actually running when you walk the parse tree.

Testing
-------
The files Tests/checktest0-7.g contain different things you need
to check for.  Specific instructions are given in each test file.

General thoughts and tips
-------------------------
The main thing you need to be thinking about with checking is program
correctness.  Does this statement or operation that you're looking at
in the parse tree make sense?  If not, some kind of error needs to be
generated.  Use your own experiences as a programmer as a guide (think
about what would cause an error in your favorite programming
language).

One challenge is going to be the management of many fiddly details. 
You've got to track symbols, types, and different sorts of capabilities.
It's not always clear how to best organize all of that.  So, expect to
fumble around a bit at first.
'''

from collections import ChainMap
from .errors import error
from .ast import *
from .typesys import Type, UnsupportedOperator

class CheckProgramVisitor(NodeVisitor):
    '''
    Program checking class.   This class uses the visitor pattern as described
    in ast.py.   You need to define methods of the form visit_NodeName()
    for each kind of AST node that you want to process.  You may need to
    adjust the method names here if you've picked different AST node names.
    '''
    def __init__(self):
        self.globals = { }
        self.locals = self.globals

        # Initialize the symbol table
        self.symbols = ChainMap(self.locals, self.globals)

        # Put the builtin type names in the symbol table
        self.globals.update(Type.builtins)

        # Current function (if any)
        self.current_function = None

    def visit_ConstDeclaration(self, node):
        self.visit(node.value)
        node.type = node.value.type

        if node.name in self.locals:
            error(node.lineno, f'{node.name} redefined. Previous definition on {self.symbols[node.name].lineno}')
        else:
            self.locals[node.name] = node

    def visit_VarDeclaration(self, node):
        self.visit(node.datatype)
        node.type = node.datatype.type

        if node.value:
            self.visit(node.value)
            if node.value.type != node.type:
                error(node.lineno, f'type error. {node.type.name} = {node.value.type.name}')

        if node.name in self.locals:
            error(node.lineno, f'{node.name} redefined. Previous definition on {self.symbols[node.name].lineno}')
        self.locals[node.name] = node

    def visit_SimpleLocation(self, node):
        if node.name not in self.symbols:
            error(node.lineno, f'{node.name} undefined')
            node.type = Type
            return 
        sym = self.symbols[node.name]
        if node.usage == 'write' and not isinstance(sym, VarDeclaration):
            error(node.lineno, f"Can't assign to {node.name}")
            node.type = Type
        elif node.usage == 'read' and not isinstance(sym, (VarDeclaration,ConstDeclaration)):
            error(node.lineno, f"Can't read from {node.name}")
            node.type = Type
        else:
            node.type = sym.type

    def visit_Assignment(self, node):
        node.location.usage = 'write'
        self.visit(node.location)
        self.visit(node.value)
        if node.location.type != node.value.type:
            error(node.lineno, f'type error. {node.location.type.name} = {node.value.type.name}')

    def visit_ReadValue(self, node):
        node.location.usage = 'read'
        self.visit(node.location)
        node.type = node.location.type

    def visit_IntegerLiteral(self, node):
        node.type = Type.lookup('int')

    def visit_FloatLiteral(self, node):
        node.type = Type.lookup('float')

    def visit_CharLiteral(self, node):
        node.type = Type.lookup('char')

    def visit_BoolLiteral(self, node):
        node.type = Type.lookup('bool')

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        try:
            node.type = node.left.type.check_binop(node.op, node.right.type)
        except UnsupportedOperator as e:
            error(node.lineno, str(e))
            
            # Discussion: Even when there's a type error, you still have to
            # assign a resultant type to the node to make subsequent type checking
            # work (otherwise, you'll get AttributeError exceptions).  For this,
            # I use just the generic "Type" class as a stand-in.
            node.type = Type

    def visit_UnaryOp(self, node):
        self.visit(node.operand)
        try:
            node.type = node.operand.type.check_unaryop(node.op)
        except UnsupportedOperator as e:
            error(node.lineno, str(e))
            node.type = Type

    def visit_SimpleType(self, node):
        try:
            node.type = Type.lookup(node.name)
        except KeyError as e:
            error(node.lineno, f'unknown type name {node.name}')
            node.type = Type

    def visit_IfStatement(self, node):
        self.visit(node.test)
        if node.test.type.name != 'bool':
            error(node.lineno, f'Conditional test not a boolean')
        self.visit(node.if_statements)
        self.visit(node.else_statements)

    def visit_WhileStatement(self, node):
        self.visit(node.test)
        if node.test.type.name != 'bool':
            error(node.lineno, f'Conditional test not a boolean')
        self.visit(node.statements)

    def visit_ReturnStatement(self, node):
        self.visit(node.value)
        if not self.current_function:
            error(node.lineno, 'return statement used outside of a function')
            return

        if node.value.type != self.current_function.type:
            error(node.lineno, f'Bad return type {node.value.type.name}. Expected {self.current_function.type.name}')

    def visit_Parm(self, node):
        self.visit(node.datatype)
        node.type = node.datatype.type
        if node.name in self.locals:
            error(node.lineno, f'Parameter {node.name} already defined')
        else:
            self.locals[node.name] = node

    def visit_FuncDeclaration(self, node):
        if self.current_function:
            error(node.lineno, f'Nested functions not allowed')
            return
        self.visit(node.return_type)
        node.type = node.return_type.type
        if node.name in self.locals:
            error(node.lineno, f'{node.name} redefined. Previous definition on {self.symbols[node.name].lineno}')
        else:
            self.locals[node.name] = node

        oldlocals = self.locals
        self.locals = { }
        self.symbols = ChainMap(self.locals, self.globals)
        self.current_function = node
        self.visit(node.parameters)
        self.visit(node.statements)
        self.locals = oldlocals
        self.symbols = ChainMap(self.locals, self.globals)
        self.current_function = None

    def visit_FuncCall(self, node):
        if node.name not in self.symbols:
            error(node.lineno, f'Function {node.name} not defined')
            node.type = Type
            return
        func = self.symbols[node.name]
        if not isinstance(func, FuncDeclaration):
            error(node.lineno, f'{node.name} is not a function')
            node.type = Type
            return
        
        self.visit(node.arguments)
        if len(node.arguments) != len(func.parameters):
            error(node.lineno, f'Function {node.name} requires {len(func.parameters)} arguments')
            
        for arg, parm in zip(node.arguments, func.parameters):
            if arg.type != parm.type:
                error(node.lineno, f'Type mismatch for parameter {parm.name}.'
                                   f'Expected {parm.type.name}. Got {arg.type.name}')

        node.type = func.type
    
# ----------------------------------------------------------------------
#                       DO NOT MODIFY ANYTHING BELOW       
# ----------------------------------------------------------------------

def check_program(ast):
    '''
    Check the supplied program (in the form of an AST)
    '''
    checker = CheckProgramVisitor()
    checker.visit(ast)

def main():
    '''
    Main program. Used for testing
    '''
    import sys
    from .parser import parse

    if len(sys.argv) < 2:
        sys.stderr.write('Usage: python3 -m gone.checker filename\n')
        raise SystemExit(1)

    ast = parse(open(sys.argv[1]).read())
    check_program(ast)
    if '--show-types' in sys.argv:
        for depth, node in flatten(ast):
            print('%s: %s%s type: %s' % (getattr(node, 'lineno', None), ' '*(4*depth), node,
                                         getattr(node, 'type', None)))

if __name__ == '__main__':
    main()



