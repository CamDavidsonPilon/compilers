# gone/typesys.py
'''
Type System
===========
This file implements basic features of the type system.  There is a
lot of flexibility possible here, but the best strategy might be to
not overthink the problem.  At least not at first.  Here are the
minimal basic requirements:

1. Types have names (e.g., 'int', 'float', 'char')
2. Types have to be comparable. (e.g., int != float).
3. Types support different operators (e.g., +, -, *, /, etc.)
'''

class UnsupportedOperator(Exception):
    pass

class Type(object):
    # These class attributes must be filled in by subclasses
    name = 'type'
    binary_ops = { }
    unary_ops = { }

    # Fake "lineno" attribute to use if a Type gets mixed up with error reporting
    lineno = '<builtin type>'

    # Tracking of builtin types
    builtins = { }
    @classmethod
    def __init_subclass__(cls):
        assert 'name' in cls.__dict__, 'name must be defined'
        assert 'binary_ops' in cls.__dict__, 'binary_ops must be defined'
        assert 'unary_ops' in cls.__dict__, 'unary_ops must be defined'
        Type.builtins[cls.name] = cls

    @classmethod
    def check_binop(cls, op, other):
        if cls is Type or other is Type:
            return Type
        result = cls.binary_ops.get((cls.name, op, other.name))
        if result:
            return cls.builtins[result]
        else:
            raise UnsupportedOperator(f'Unsupported operation {cls.name} {op} {other.name}')

    @classmethod
    def check_unaryop(cls, op):
        if cls is Type:
            return Type
        result = cls.unary_ops.get((op, cls.name))
        if result:
            return cls.builtins[result]
        else:
            raise UnsupportedOperator(f'Unsupported operation {op} {cls.name}')

    @classmethod
    def lookup(cls, name):
        return cls.builtins[name]

class IntType(Type):
    name = 'int'
    binary_ops = {
        ('int', '+', 'int') : 'int',
        ('int', '-', 'int') : 'int',
        ('int', '*', 'int') : 'int',
        ('int', '/', 'int') : 'int',
        }
    unary_ops = {
        ('+', 'int') : 'int',
        ('-', 'int') : 'int'
        }

class FloatType(Type):
    name = 'float'
    binary_ops = {
        ('float', '+', 'float') : 'float',
        ('float', '-', 'float') : 'float',
        ('float', '*', 'float') : 'float',
        ('float', '/', 'float') : 'float',
        }
    unary_ops = {
        ('+', 'float') : 'float',
        ('-', 'float') : 'float'
        }

class CharType(Type):
    name = 'char'
    binary_ops = { }
    unary_ops = { }

if __name__ == '__main__':
    a = Type.lookup('int')
    b = Type.lookup('int')
    c = a.check_binop('+', b)
    assert c == IntType
    d = a.check_unaryop('-')
    assert d == IntType

    





          




