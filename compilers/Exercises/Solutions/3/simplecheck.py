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

# Part (a) - AST Walking
class SimpleCheck(ast.NodeVisitor):
    def visit_Name(self,  node):
        print(node.id, node.ctx)


SimpleCheck().visit(top)

# Part (b) - Symbol tables

class SimpleCheck(ast.NodeVisitor):
    def __init__(self):
        self.symbols = set()

    def visit_Name(self, node):
        # If storing, a name is added to the symbol table
        if isinstance(node.ctx, ast.Store):
            self.symbols.add(node.id)

        # If loading, check for definition in the symbol table
        elif isinstance(node.ctx, ast.Load):
            if node.id not in self.symbols:
                print('Error: Name %s not defined' % node.id)

SimpleCheck().visit(top)

# Part (c) - Introducing a Type System

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

        # For each target, set the symbol table to the value type
        self.assignment_value = node.value
        for target in node.targets:
            self.visit(target)
            
    def visit_Name(self, node):
        # If storing, a type is added to the symbol table
        if isinstance(node.ctx, ast.Store):
            self.symbols[node.id] = getattr(self.assignment_value, 'type', None)

        # If loading, check for definition in the symbol table
        elif isinstance(node.ctx, ast.Load):
            if node.id not in self.symbols:
                print('Error: Name %s not defined' % node.id)

checker = SimpleCheck()
checker.visit(top)
print(checker.symbols)

# Part (d) - Type Propagation

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

        # Visit the targets to set symbol table and assign known types
        self.assignment_value = node.value
        for target in node.targets:
            self.visit(target)
            
    def visit_Name(self, node):
        # If storing, a type is added to the symbol table
        if isinstance(node.ctx, ast.Store):
            self.symbols[node.id] = getattr(self.assignment_value, 'type', None)

        # If loading, check for definition and set the type attribute
        elif isinstance(node.ctx, ast.Load):
            if node.id not in self.symbols:
                print('Error: Name %s not defined' % node.id)
            else:
                node.type = self.symbols.get(node.id, None)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        # Propagate the type to the result
        node.type = getattr(node.left, 'type', None)

checker = SimpleCheck()
checker.visit(top)
print(checker.symbols)

# Part (e) - Type Checking

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

        # Visit the targets to set symbol table and assign known types
        self.assignment_value = node.value
        for target in node.targets:
            self.visit(target)
            
    def visit_Name(self, node):
        # If storing, a symbol is added to the symbol table
        if isinstance(node.ctx, ast.Store):
            self.symbols[node.id] = getattr(self.assignment_value, 'type', None)

        # If loading, a symbol is loaded from the symbol table
        elif isinstance(node.ctx, ast.Load):
            if node.id not in self.symbols:
                print('Error: Name %s not defined' % node.id)
            else:
                node.type = self.symbols.get(node.id, None)

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

checker = SimpleCheck()
checker.visit(top)
print(checker.symbols)


# Part (f) - Type Checking

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
    def __init__(self):
        self.symbols = { }

    def visit_Num(self, node):
        node.type = 'num'

    def visit_Str(self, node):
        node.type = 'str'

    def visit_Assign(self, node):
        # Visit the right-hand-side value to get types assignment
        self.visit(node.value)

        # Visit the targets to set symbol table and assign known types
        self.assignment_value = node.value
        for target in node.targets:
            self.visit(target)
            
    def visit_Name(self, node):
        # If storing, a symbol is added to the symbol table
        if isinstance(node.ctx, ast.Store):
            self.symbols[node.id] = getattr(self.assignment_value, 'type', None)

        # If loading, a symbol is loaded from the symbol table
        elif isinstance(node.ctx, ast.Load):
            if node.id not in self.symbols:
                print('Error: Name %s not defined' % node.id)
            else:
                node.type = self.symbols.get(node.id, None)

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

checker = SimpleCheck()
checker.visit(top)
print(checker.symbols)





