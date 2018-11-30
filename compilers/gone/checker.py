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

from .errors import error
from .ast import *
from .typesys import check_binop, check_unaryop, INT, FLOAT, CHAR, ERROR, \
                     builtin_types, TUPLE, tuple_type, BOOL
from collections import ChainMap

MUTABLE = 1
IMMUTABLE = 0

class CheckProgramVisitor(NodeVisitor):
    '''
    Program checking class.   This class uses the visitor pattern as described
    in ast.py.   You need to define methods of the form visit_NodeName()
    for each kind of AST node that you want to process.  You may need to
    adjust the method names here if you've picked different AST node names.
    '''
    def __init__(self):
        # Initialize the symbol table
        self.global_symbols = ChainMap()

    def visit_FunctionDeclaration(self, node):

        # first check if it's not already defined.
        if node.name in builtin_types:
            error(node.lineno, "Redeclaration of builtin keyword %s" % node.name)

        if node.name in self.global_symbols:
            # check if lineno is present
            error(node.lineno, "Redeclaration of existing constant %s" % node.name)
            return

        # let's seed the global symbols with the parameter list

        local_context = self.global_symbols.new_child()
        for argument in node.arguments:
            self.visit(argument)
            local_context[argument.name] = argument

        node.statements.local_context = local_context
        # okay, we want to check the internal statements next
        self.visit(node.statements)


        # set the type to be the return type
        self.visit(node.return_type)

        node.type = node.return_type.type

        if local_context[node.return_name].type != node.type:
            error(node.lineno, "Function %s should return type '%s', but variable %s is type '%s'" % (node.name, node.type, node.return_name, local_context[node.return_name].type))
            return

        self.global_symbols[node.name] = node


    def visit_FunctionCall(self, node):
        self.visit(node.name)
        self.visit(node.params)
        function = self.global_symbols[node.name.name]
        node.type = function.type

        # make sure that arguments and params are the right type
        # check length too eventually
        if len(node.params) != len(function.arguments):
            error("Arugment list is not the same size as parameters given")

        for (param, argument) in zip(node.params, function.arguments):
            if param.type != argument.type:
                error(node.lineno, "Argument %s was expecting type '%s', but see type '%s'" % (argument.name, argument.type, param.type))


    def visit_Parameter(self, node):
        self.visit(self.decorate_with_local_context(node, node.value))
        node.type = node.value.type

    def visit_Statements(self, node):
        for child_node in node.statements:
            self.visit(self.decorate_with_local_context(node, child_node))

    @staticmethod
    def decorate_with_local_context(parent, child):
        if hasattr(parent, 'local_context'):
            child.local_context = parent.local_context
        return child

    def visit_FunctionArgument(self, node):
        self.visit(node.datatype)
        node.type = node.datatype.type


    def visit_ConstDeclaration(self, node):
        # For a declaration, you'll need to check that it isn't already defined.
        # You'll put the declaration into the symbol table so that it can be looked up later
        symbols = getattr(node, 'local_context', self.global_symbols)

        self.visit(self.decorate_with_local_context(node, node.value))
        if node.name in builtin_types:
            error(node.lineno, "Redeclaration of builtin keyword %s" % node.name)

        if node.name in symbols:
            # check if lineno is present
            error(node.lineno, "Redeclaration of existing constant %s" % node.name)
            return

        node.usage = IMMUTABLE
        node.type = node.value.type
        symbols[node.name] = node

    def visit_VarDeclaration(self, node):
        # For a declaration, you'll need to check that it isn't already defined.
        # You'll put the declaration into the symbol table so that it can be looked up later
        symbols = getattr(node, 'local_context', self.global_symbols)


        self.visit(self.decorate_with_local_context(node, node.datatype))
        self.visit(self.decorate_with_local_context(node, node.value))

        if node.name in builtin_types:
            error(node.lineno, "Redeclaration of builtin keyword %s" % node.name)

        if node.name in symbols:
            # check if lineno is present
            error(node.lineno, "Redeclaration of existing variable %s" % node.name)
            return

        if node.value and node.datatype.type != node.value.type:
            error(node.lineno, "Variable %s declared as type '%s', but assigned value of type '%s'" % (node.name, node.datatype.type, node.value.type))
            return

        node.type = node.datatype.type
        node.usage = MUTABLE
        symbols[node.name] = node

    def visit_SimpleLocation(self, node):
        # A location represents a place where you can read/write a value.
        # You'll need to consult the symbol table to find out information about it

        symbols = getattr(node, 'local_context', self.global_symbols)


        if node.name not in symbols:
            # check if lineno is present
            error(node.lineno, "Variable %s is not defined" % node.name)
            node.type = ERROR
            return
        node.type = symbols[node.name].type

    def visit_IfConditional(self, node):
        self.visit(self.decorate_with_local_context(node, node.switch))
        if node.switch.type != BOOL:
            error(node.lineno, "if switch statement should be type 'bool'.")
            return
        self.visit(self.decorate_with_local_context(node, node.true_path))

        if node.false_path:
            self.visit(self.decorate_with_local_context(node, node.false_path))


    def visit_WhileConditional(self, node):
        self.visit(node.switch)
        if node.switch.type != BOOL:
            error(node.lineno, "while switch statement should be type 'bool'.")
            return
        self.visit(node.statements)

    def visit_Assignment(self, node):
        self.visit(self.decorate_with_local_context(node, node.value))
        self.visit(self.decorate_with_local_context(node, node.location))

        symbols = getattr(node, 'local_context', self.global_symbols)

        if node.location.name not in symbols:
            return

        location = symbols[node.location.name]
        if location.usage == IMMUTABLE:
            node.type = ERROR
            error(node.lineno, "Variable %s is not mutable" % node.location.name)
            return

        if node.location.type != node.value.type:
            error(node.lineno, "Variable %s declared as type '%s', but assigned value of type '%s'" % (node.location.name, node.location.type, node.value.type))
            node.type = ERROR
            return

        node.type = node.location.type

    def visit_IntegerLiteral(self, node):
        node.type = INT

    def visit_BoolLiteral(self, node):
        node.type = BOOL

    def visit_FloatLiteral(self, node):
        node.type = FLOAT

    def visit_CharLiteral(self, node):
        node.type = CHAR


    def visit_BinOp(self, node):
        # For operators, you need to visit each operand separately.  You'll
        # then need to make sure the types and operator are all compatible.
        self.visit(self.decorate_with_local_context(node, node.left))
        self.visit(self.decorate_with_local_context(node, node.right))

        lnode = node.left
        rnode = node.right

        if check_binop(lnode.type, node.op, rnode.type)== ERROR:
            error(node.lineno, "unsupported operand type(s) for %s: '%s' and '%s'" % (node.op, lnode.type, rnode.type))
        node.type = check_binop(lnode.type, node.op, rnode.type)

    def visit_UnaryOp(self, node):
        # For operators, you need to visit each operand separately.  You'll
        # then need to make sure the types and operator are all compatible.
        self.visit(self.decorate_with_local_context(node, node.right))

        rnode = node.right

        if check_unaryop(node.op, rnode.type) == ERROR:
            error(node.lineno, "unsupported operand type(s) for %s: '%s'" % (node.op, rnode.type))
        node.type = check_unaryop(node.op, rnode.type)

    def visit_PrintStatement(self, node):
        self.visit(self.decorate_with_local_context(node, node.value))

    def visit_SimpleType(self, node):
        # Associate a type name such as "int" with a Type object
        node.type = node.name
        if (node.name not in self.global_symbols) and (node.name not in builtin_types):
            # check if lineno is present
            error(node.lineno, "Variable %s is not defined." % node.name)
            return


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




