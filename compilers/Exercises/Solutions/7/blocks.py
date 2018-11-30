# blocks.py
#
# An example of how to create basic blocks, control flow graphs,
# and low-level code using Python ASTs.

import ast
class CodeGenerator(ast.NodeVisitor):
    '''
    Sample code generator with basic blocks and control flow
    '''
    def __init__(self):
        self.code = []
        self._label = 0

    def new_block(self):
        self._label += 1
        return 'b%d' % self._label

    def visit_If(self,node):
        '''
        Example of compiling a simple Python if statement. 
        '''
        # Step 1: Evaluate the test condition
        self.visit(node.test)

        # Step 2: Make a block labels for both branches and the merge point
        ifblock = self.new_block()
        elseblock = self.new_block()
        mergeblock = self.new_block()

        self.code.append(('JUMP_IF_FALSE', elseblock))
        self.code.append(('BLOCK', ifblock))

        # Step 4: Traverse all of the statements in the if-body
        for bnode in node.body:
            self.visit(bnode)
        self.code.append(('JUMP', mergeblock))

        # Step 5: If there's an else-clause, create a new block and traverse statements
        if node.orelse:
            self.code.append(('BLOCK', elseblock))
            # Visit the body of the else-clause
            for bnode in node.orelse:
                self.visit(bnode)

        # Step 6: Start a new block to continue on with more instructions
        self.code.append(('BLOCK', mergeblock))

    def visit_While(self, node):
        testblock = self.new_block()
        exitblock = self.new_block()

        self.code.append(('BLOCK', testblock))
        self.visit(node.test)
        self.code.append(('JUMP_IF_FALSE', exitblock))
        for bnode in node.body:
            self.visit(bnode)
        self.code.append(('JUMP', testblock))
        self.code.append(('BLOCK', exitblock))

    def visit_BinOp(self,node):
        self.visit(node.left)
        self.visit(node.right)
        opname = node.op.__class__.__name__
        inst = ("BINARY_"+opname.upper(),)
        self.code.append(inst)

    def visit_Compare(self,node):
        self.visit(node.left)
        opname = node.ops[0].__class__.__name__
        self.visit(node.comparators[0])
        inst = ("BINARY_"+opname.upper(),)
        self.code.append(inst)

    def visit_Assign(self, node):
        self.visit(node.value)
        for t in node.targets:
            self.visit(t)

    def visit_Name(self,node):
        if isinstance(node.ctx, ast.Load):
            inst = ('LOAD_GLOBAL',node.id)
        else:
            inst = ('STORE_GLOBAL', node.id)
        self.code.append(inst)

    def visit_Num(self,node):
        inst = ('LOAD_CONST',node.n)
        self.code.append(inst)

if __name__ == '__main__':
    top = ast.parse("""\
start
if a < 0:
   a + b
else:
   a - b
done

while n > 0:
    n = n - 1
""")

    gen = CodeGenerator()
    gen.visit(top)

    for inst in gen.code:
        print(inst)
