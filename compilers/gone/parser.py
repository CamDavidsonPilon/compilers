# gone/parser.py
'''
Project 2:  Write a parser
==========================
In this project, you write the basic shell of a parser for Gone.  A
formal BNF of the language follows.  Your task is to write parsing
rules and build the AST for this grammar using SLY.  The following
grammar is partial.  More features get added in later projects.

program : statements
        | empty

statements :  statements statement
           |  statement

statement :  const_declaration
          |  var_declaration
          |  assign_statement
          |  print_statement

const_declaration : CONST ID = expression ;

var_declaration : VAR ID datatype ;
                | VAR ID datatype = expression ;

assign_statement : location = expression ;

print_statement : PRINT expression ;

expression :  + expression
           |  - expression
           | expression + expression
           | expression - expression
           | expression * expression
           | expression / expression
           | ( expression )
           | location
           | literal

literal : INTEGER
        | FLOAT
        | CHAR
        | BOOL

location : ID
         ;

datatype : ID
         ;

empty    :

To do the project, follow the instructions contained below.
'''

# ----------------------------------------------------------------------
# parsers are defined using SLY.  You inherit from the Parser class
#
# See http://sly.readthedocs.io/en/latest/
# ----------------------------------------------------------------------
from sly import Parser

# ----------------------------------------------------------------------
# The following import loads a function error(lineno,msg) that should be
# used to report all error messages issued by your parser.  Unit tests and
# other features of the compiler will rely on this function.  See the
# file errors.py for more documentation about the error handling mechanism.
from .errors import error

# ----------------------------------------------------------------------
# Import the lexer class.  It's token list is needed to validate and
# build the parser object.
from .tokenizer import GoneLexer

# ----------------------------------------------------------------------
# Get the AST nodes.
# Read instructions in ast.py
from .ast import *

class GoneParser(Parser):
    # Same token set as defined in the lexer
    tokens = GoneLexer.tokens
    # ----------------------------------------------------------------------
    # Operator precedence table.   Operators must follow the same
    # precedence rules as in Python.  Instructions to be given in the project.

    precedence = (
        ('left', 'AND', 'OR'),
        ('nonassoc', 'LT', 'GT', 'LE', 'GE', 'EQ', 'NQ'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'NOT'),
    )

    # ----------------------------------------------------------------------
    # YOUR TASK.   Translate the BNF in the string below into a collection
    # of parser functions.  For example, a rule such as :
    #
    #   program : statements
    #
    # Gets turned into a Python method like this:
    #
    # @_('statements')
    # def program(self, p):
    #      return Program(p.statements)
    #
    # For symbols such as '(' or '+', you'll need to replace with the name
    # of the corresponding token such as LPAREN or PLUS.
    #
    # In the body of each rule, create an appropriate AST node and return it
    # as shown above.
    #
    # For the purposes of lineno number tracking, you should assign a line number
    # to each AST node as appropriate.  To do this, I suggest pulling the
    # line number off of any nearby terminal symbol.  For example:
    #
    # @_('PRINT expr SEMI')
    # def print_statement(self, p):
    #     return PrintStatement(p.expr, lineno=p.lineno)
    #
    # STARTING OUT
    # ============
    # The following grammar rules should give you an idea of how to start.
    # Try running this file on the input Tests/parsetest0.g
    #
    # Afterwards, add features by looking at the code in Tests/parsetest1-6.g

    @_('statements statement')
    def statements(self, p):               # Multiple statements
        p.statements.append(p.statement)   # Add a statement to previous statements
        return p.statements

    @_('statement')
    def statements(self, p):               # A single statement
        # lineno are broken here because statements don't really have a line...
        return Statements([p.statement], lineno=p.statement.lineno)

    @_('PRINT expression SEMI')
    def print_statement(self, p):
        return PrintStatement(p.expression, lineno=p.lineno)

    @_('print_statement',
       'const_declaration',
       'var_declaration',
       'assign_statement',
       'if_statement',
       'while_statement',
       'function_declaration',
      )
    def statement(self, p):
        return p[0]

    @_('LPAREN statement RPAREN')
    def statement(self, p):
        return p.statement

    @_('expression PLUS expression',
       'expression TIMES expression',
       'expression MINUS expression',
       'expression DIVIDE expression',
       'expression GT expression',
       'expression OR expression',
       'expression LT expression',
       'expression EQ expression',
       'expression AND expression',
       'expression GE expression',
       'expression LE expression',
       'expression NQ expression',
       )
    def expression(self, p):
        # I may want to map things like '<=' to 'LT'...
        return BinOp(p[1], p.expression0, p.expression1, lineno=p.lineno)

    @_('PLUS expression',
       'MINUS expression',
       'NOT expression')
    def expression(self, p):
        return UnaryOp(p[0], p[1], lineno=p.lineno)

    @_('literal')
    def expression(self, p):
        return p.literal

    @_('location')
    def expression(self, p):
        return p.location

    @_('ID LPAREN params RPAREN')
    def expression(self, p):
        # function call
        return FunctionCall(SimpleLocation(p.ID, lineno=p.lineno), p.params, lineno=p.lineno)

    @_('ID LPAREN RPAREN')
    def expression(self, p):
        # function call
        return FunctionCall(SimpleLocation(p.ID, lineno=p.lineno), [], lineno=p.lineno)


    @_('params COMMA param')
    def params(self, p):
        p.params.append(p.param)
        return p.params

    @_('param')
    def params(self, p):
        return [p.param]

    @_('expression')
    def param(self, p):
        return Parameter(p.expression, lineno=p.expression.lineno)

    @_('ID')
    def location(self, p):
        return SimpleLocation(p.ID, lineno=p.lineno)

    @_('INTEGER')
    def literal(self, p):
        return IntegerLiteral(int(p.INTEGER), lineno=p.lineno)

    @_('BOOL')
    def literal(self, p):
        return BoolLiteral(p.BOOL, lineno=p.lineno)


    @_('FLOAT')
    def literal(self, p):
        return FloatLiteral(float(p.FLOAT), lineno=p.lineno)

    @_('CHAR')
    def literal(self, p):
        return CharLiteral(eval(p.CHAR), lineno=p.lineno)

    @_('LPAREN expression RPAREN')
    def expression(self, p):
        return p.expression

    @_('CONST ID ASSIGN literal SEMI')
    def const_declaration(self, p):
        return ConstDeclaration(p.ID, p.literal, lineno=p.lineno)

    @_('VAR ID datatype ASSIGN expression SEMI')
    def var_declaration(self, p):
        return VarDeclaration(p.ID, p.datatype, p.expression, lineno=p.lineno)

    @_('VAR ID datatype SEMI')
    def var_declaration(self, p):
        return VarDeclaration(p.ID, p.datatype, None, lineno=p.lineno)

    @_('ID')
    def datatype(self, p):
        return SimpleType(p.ID, lineno=p.lineno)

    @_('IF expression LCURLY statements RCURLY ELSE LCURLY statements RCURLY')
    def if_statement(self, p):
        return IfConditional(p.expression, p.statements0, p.statements1, lineno=p.lineno)


    @_('IF expression LCURLY statements RCURLY')
    def if_statement(self, p):
        return IfConditional(p.expression, p.statements, None, lineno=p.lineno)

    @_('WHILE expression LCURLY statements RCURLY')
    def while_statement(self, p):
        return WhileConditional(p.expression, p.statements, lineno=p.lineno)

    @_('FUNCTION ID LPAREN arguments RPAREN ID LCURLY statements RETURN ID RCURLY')
    def function_declaration(self, p):
        return FunctionDeclaration(
            p.ID0,
            p.arguments,
            SimpleType(p.ID1, lineno=p.lineno),
            p.statements,
            p.ID2,
        lineno=p.lineno)

    @_('FUNCTION ID LPAREN RPAREN ID LCURLY statements RETURN ID RCURLY')
    def function_declaration(self, p):
        return FunctionDeclaration(
            p.ID0,
            [],
            SimpleType(p.ID1, lineno=p.lineno),
            p.statements,
            p.ID2,
        lineno=p.lineno)

    @_('arguments COMMA argument')
    def arguments(self, p):
        p.arguments.append(p.argument)
        return p.arguments

    @_('argument')
    def arguments(self, p):
        return [p.argument]

    @_('ID datatype')
    def argument(self, p):
        return FunctionArgument(p.ID, p.datatype, lineno=p.lineno) # TODO

    @_('ID LPAREN ID RPAREN')
    def datatype(self, p):
        # for tuple declarations
        return TupleType(p.ID0, SimpleType(p.ID1, lineno=p.lineno), lineno=p.lineno)

    @_('location ASSIGN expression SEMI')
    def assign_statement(self, p):
        return Assignment(p.location, p.expression, lineno=p.lineno)

    @_('location ASSIGN location ASSIGN expression SEMI')
    def assign_statement(self, p):
        return [ Assignment(p.location0, p.expression, lineno=p.lineno),
                 Assignment(p.location1, p.expression, lineno=p.lineno)]

    @_('location COMMA location ASSIGN expression COMMA expression SEMI')
    def assign_statement(self, p):
        # x, y = y, x;
        # x, y = 1, 1 + 2;
        return [ Assignment(p.location0, p.expression0, lineno=p.lineno),
                 Assignment(p.location1, p.expression1, lineno=p.lineno)]

    @_('location PLUS ASSIGN expression SEMI')
    @_('location TIMES ASSIGN expression SEMI')
    @_('location DIVIDE ASSIGN expression SEMI')
    @_('location MINUS ASSIGN expression SEMI')
    def assign_statement(self, p):
        # x += 1;
        return Assignment(p.location,
                          BinOp(p[1], p.location, p.expression, lineno=p.lineno),
                          lineno=p.lineno)

    @_('location PLUS PLUS SEMI')
    @_('location MINUS MINUS SEMI')
    def assign_statement(self, p):
        # x ++;
        return Assignment(p.location,
                          BinOp(p[1], p.location, IntegerLiteral(1, lineno=p.lineno), lineno=p.lineno),
                          lineno=p.lineno)



    # ----------------------------------------------------------------------
    # DO NOT MODIFY
    #
    # catch-all error handling.   The following function gets called on any
    # bad input.  p is the offending token or None if end-of-file (EOF).
    def error(self, p):
        if p:
            error(p.lineno, "Syntax error in input at token '%s'" % p.value)
        else:
            error('EOF','Syntax error. No more input.')



# ----------------------------------------------------------------------
#                     DO NOT MODIFY ANYTHING BELOW HERE
# ----------------------------------------------------------------------

def parse(source):
    '''
    Parse source code into an AST. Return the top of the AST tree.
    '''
    lexer = GoneLexer()
    parser = GoneParser()
    ast = parser.parse(lexer.tokenize(source))
    return ast

def main():
    '''
    Main program. Used for testing.
    '''
    import sys

    if len(sys.argv) != 2:
        sys.stderr.write('Usage: python3 -m gone.parser filename\n')
        raise SystemExit(1)

    # Parse and create the AST
    ast = parse(open(sys.argv[1]).read())
    # Output the resulting parse tree structure
    for depth, node in flatten(ast):
       print('%s: %s%s' % (getattr(node, 'lineno', None), ' '*(4*depth), node))

if __name__ == '__main__':
    main()
