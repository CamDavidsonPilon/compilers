# gone/typesys.py
'''
Gone Type System
================
This file implements basic features of the Gone type system.  There is
a lot of flexibility possible here, but the best strategy might be to
not overthink the problem.  At least not at first.  Here are the
minimal basic requirements:

1. Types have names (e.g., 'int', 'float', 'char')
2. Types have to be comparable. (e.g., int != float).
3. Types support different operators (e.g., +, -, *, /, etc.)

To deal with all this initially, I'd recommend representing types
as simple strings.  Make tables that represent the capabilities
of different types. Make some utility functions that check operators.
KEEP IT SIMPLE. REPEAT. SIMPLE.

'''

# List of builtin types.  These will get added to the symbol table
INT = 'int'
FLOAT = 'float'
CHAR = 'char'
TUPLE = 'tuple'
ERROR = 'error'
BOOL = 'bool'

builtin_types = [ INT, FLOAT, CHAR, ERROR, TUPLE, BOOL]

# Dict mapping all valid binary operations to a result type
_supported_binops = {
    (INT, '+', INT) : INT,
    (INT, '-', INT) : INT,
    (INT, '*', INT) : INT,
    (INT, '/', INT) : INT, # we are going to copy Python 2 division fuck it.
    (INT, '>', INT) : BOOL,
    (INT, '>=', INT) : BOOL,
    (INT, '<', INT) : BOOL,
    (INT, '<=', INT) : BOOL,
    (INT, '!=', INT) : BOOL,
    (INT, '==', INT) : BOOL,



    (FLOAT, '-', FLOAT) : FLOAT,
    (FLOAT, '+', FLOAT) : FLOAT,
    (FLOAT, '*', FLOAT) : FLOAT,
    (FLOAT, '/', FLOAT) : FLOAT,
    (FLOAT, '>', FLOAT) : BOOL,
    (FLOAT, '>=', FLOAT) : BOOL,
    (FLOAT, '<', FLOAT) : BOOL,
    (FLOAT, '<=', FLOAT) : BOOL,
    (FLOAT, '!=', FLOAT) : BOOL,
    (FLOAT, '==', FLOAT) : BOOL,

    (INT, '>',  FLOAT) : BOOL,
    (INT, '>=', FLOAT) : BOOL,
    (INT, '<',  FLOAT) : BOOL,
    (INT, '<=', FLOAT) : BOOL,
    (INT, '!=', FLOAT) : BOOL,
    (INT, '==', FLOAT) : BOOL,

    (FLOAT, '>',  INT) : BOOL,
    (FLOAT, '>=', INT) : BOOL,
    (FLOAT, '<',  INT) : BOOL,
    (FLOAT, '<=', INT) : BOOL,
    (FLOAT, '!=', INT) : BOOL,
    (FLOAT, '==', INT) : BOOL,

    (FLOAT, '*', INT) : FLOAT,
    (INT, '*', FLOAT) : FLOAT,

    (BOOL, '==', BOOL) : BOOL,
    (BOOL, '!=', BOOL) : BOOL,
    (BOOL, '&&', BOOL) : BOOL,
    (BOOL, '||', BOOL) : BOOL,


    (CHAR, '==', CHAR): BOOL,
    (CHAR, '!=', CHAR): BOOL,
    }

# Dict mapping all valid unary operations to result type
_supported_unaryops = {
    ('-', INT) : INT,
    ('+', INT) : INT,
    ('-', FLOAT) : FLOAT,
    ('+', FLOAT) : FLOAT,
    ('!', BOOL) : BOOL,
    }

def check_binop(left_type, op, right_type):
    '''
    Check the validity of a binary operator.
    '''
    return _supported_binops.get((left_type, op, right_type), ERROR)

def check_unaryop(op, type):
    '''
    Check the validity of a unary operator.
    '''
    return _supported_unaryops.get((op, type), ERROR)


def tuple_type(value_type):
    return TUPLE + '(' + value_type + ')'







