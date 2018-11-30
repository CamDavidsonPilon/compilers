# gone/ircode.py
'''
Project 4
=========
In this project, you are going to turn the AST into an intermediate
machine code based on 3-address code. There are a few important parts
you'll need to make this work.  Please read carefully before
beginning:

A "Virtual" Machine
===================
A CPU typically consists of registers and a small set of basic opcodes
for performing mathematical calculations, loading/storing values from
memory, and basic control flow (branches, jumps, etc.).  For example,
suppose you want to evaluate an operation like this:

    a = 2 + 3 * 4 - 5

On a CPU, it might be decomposed into low-level instructions like this:

    MOVI   #2, R1
    MOVI   #3, R2
    MOVI   #4, R3
    MULI   R2, R3, R4
    ADDI   R4, R1, R5
    MOVI   #5, R6
    SUBI   R5, R6, R7
    STOREI R7, "a"

Each instruction represents a single operation such as add, multiply, etc.
There are always two input operands and a destination.  

CPUs also feature a small set of core datatypes such as integers and
floats.  There are dedicated instructions for each type.  For example:

    ADDI   R1, R2, R3        ; Integer add
    ADDF   R4, R5, R6        ; Float add

Here is an instruction set specification for our IRCode:

    MOVI   value, target     ;  Load a literal integer
    VARI   name              ;  Declare an integer variable 
    LOADI  name, target      ;  Load an integer from a variable
    STOREI target, name      ;  Store an integer into a variable
    ADDI   r1, r2, target    ;  target = r1 + r2
    SUBI   r1, r2, target    ;  target = r1 - r2
    MULI   r1, r2, target    ;  target = r1 * r2
    DIVI   r1, r2, target    ;  target = r1 / r2
    PRINTI source            ;  print source  (debugging)

    MOVF   value, target     ;  Load a literal float
    VARF   name              ;  Declare an float variable 
    LOADF  name, target      ;  Load a float from a variable
    STOREF target, name      ;  Store a float into a variable
    ADDF   r1, r2, target    ;  target = r1 + r2
    SUBF   r1, r2, target    ;  target = r1 - r2
    MULF   r1, r2, target    ;  target = r1 * r2
    DIVF   r1, r2, target    ;  target = r1 / r2
    PRINTF source            ;  print source (debugging)

    MOVB   value, target     ; Load a literal byte
    LOADB  name, target      ; Load a byte from a variable
    STOREB target, name      ; Store a byte into a variable
    PRINTB source            ; print source (debugging)

Single Static Assignment
========================
On a real CPU, there are a limited number of CPU registers.
In our virtual memory, we're going to assume that the CPU
has an infinite number of registers available.  Moreover,
we'll assume that each register can only be assigned once.
This particular style is known as Static Single Assignment (SSA).
As you generate instructions, you'll keep a running counter
that increments each time you need a temporary variable.
The example in the previous section illustrates this.

Your Task
=========
Your task is as follows: Write a AST Visitor() class that takes a
program and flattens it to a single sequence of SSA code instructions
represented as tuples of the form 

       (operation, operands, ..., destination)

Testing
=======
The files Tests/irtest0-5.g contain some input text along with
sample output. Work through each file to complete the project.
'''

from . import ast

class GenerateCode(ast.NodeVisitor):
    '''
    Node visitor class that creates 3-address encoded instruction sequences.
    '''
    def __init__(self):
        # counter for registers
        self.register_count = 0

        # The generated code (list of tuples)
        self.code = []

    def new_register(self):
         '''
         Creates a new temporary register
         '''
         self.register_count += 1
         return f'R{self.register_count}'

    # You must implement visit_Nodename methods for all of the other
    # AST nodes.  In your code, you will need to make instructions
    # and append them to the self.code list.
    #
    # A few sample methods follow.  You may have to adjust depending
    # on the names and structure of your AST nodes.

    def visit_IntegerLiteral(self, node):
        target = self.new_register()
        self.code.append(('MOVI', node.value, target))

        # Save the name of the register where the value was placed
        node.register = target

    def visit_FloatLiteral(self, node):
        target = self.new_register()
        self.code.append(('MOVF', node.value, target))
        node.register = target

    def visit_CharLiteral(self, node):
        target = self.new_register()
        self.code.append(('MOVB', ord(node.value), target))
        node.register = target

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        op = node.op
        if node.type.name == 'int':
            if op == '+':
                code = 'ADDI'
            elif op == '-':
                code = 'SUBI'
            elif op == '*':
                code = 'MULI'
            elif op == '/':
                code = 'DIVI'
            else:
                raise RuntimeError(f'Unknown binop {op}')
        elif node.type.name == 'float':
            if op == '+':
                code = 'ADDF'
            elif op == '-':
                code = 'SUBF'
            elif op == '*':
                code = 'MULF'
            elif op == '/':
                code = 'DIVF'
            else:
                raise RuntimeError(f'Unknown binop {op}')

        target = self.new_register()
        inst = (code, node.left.register, node.right.register, target)
        self.code.append(inst)
        node.register = target
        
    def visit_UnaryOp(self, node):
        self.visit(node.operand)
        if node.op == '-' and node.type.name == 'int':
            zero = self.new_register()
            target = self.new_register()
            self.code.append(('MOVI', 0, zero))
            self.code.append(('SUBI', zero, node.operand.register, target))
            node.register = target
        elif node.op == '-' and node.type.name == 'float':
            zero = self.new_register()
            target = self.new_register()
            self.code.append(('MOVF', 0.0, zero))
            self.code.append(('SUBF', zero, node.operand.register, target))
            node.register = target
        else:
            node.register = node.operand.register

    # CHALLENGE:  Figure out some more sane way to refactor the code for
    # binary and unary operators

    def visit_PrintStatement(self, node):
        self.visit(node.value)
        if node.value.type.name == 'int':
            code = 'PRINTI'
        elif node.value.type.name == 'float':
            code = 'PRINTF'
        elif node.value.type.name == 'char':
            code = 'PRINTB'
        inst = (code, node.value.register)
        self.code.append(inst)

    def emit_declaration(self, node):
        if node.value:
            self.visit(node.value)
        if node.type.name == 'int':
            code = 'VARI'
            store = 'STOREI'
        elif node.type.name == 'float':
            code = 'VARF'
            store = 'STOREF'
        elif node.type.name == 'char':
            code = 'VARB'
            store = 'STOREB'
        else:
            raise RuntimeError(f'Unsupported type {node.type}')
        self.code.append((code, node.name))
        if node.value:
            self.code.append((store, node.value.register, node.name))

    visit_ConstDeclaration = emit_declaration
    visit_VarDeclaration = emit_declaration

    def visit_SimpleLocation(self, node):
        if node.usage == 'read':
            if node.type.name == 'int':
                code = 'LOADI'
            elif node.type.name == 'float':
                code = 'LOADF'
            elif node.type.name == 'char':
                code = 'LOADB'
            else:
                raise RuntimeError(f'Unsupported type {node.type}')
            target = self.new_register()
            self.code.append((code, node.name, target))
            node.register = target
        elif node.usage == 'write':
            if node.type.name == 'int':
                code = 'STOREI'
            elif node.type.name == 'float':
                code = 'STOREF'
            elif node.type.name == 'char':
                code = 'STOREB'
            else:
                raise RuntimeError(f'Unsupported type {node.type}')
            # Note: For storing, it's assumed that the register
            # was already attached to this node. See the assignment code
            self.code.append((code, node.register, node.name))

    def visit_ReadValue(self, node):
        self.visit(node.location)
        node.register = node.location.register

    def visit_Assignment(self, node):
        self.visit(node.value)
        # Propagate the value to the location and visit
        node.location.register = node.value.register
        self.visit(node.location)

# ----------------------------------------------------------------------
#                          TESTING/MAIN PROGRAM
#
# Note: Some changes will be required in later projects.
# ----------------------------------------------------------------------

def compile_ircode(source):
    '''
    Generate intermediate code from source.
    '''
    from .parser import parse
    from .checker import check_program
    from .errors import errors_reported

    ast = parse(source)
    check_program(ast)

    # If no errors occurred, generate code
    if not errors_reported():
        gen = GenerateCode()
        gen.visit(ast)
        return gen.code    
    else:
        return []

def main():
    import sys

    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python3 -m gone.ircode filename\n")
        raise SystemExit(1)

    source = open(sys.argv[1]).read()
    code = compile_ircode(source)

    for instr in code:
        print(instr)

if __name__ == '__main__':
    main()
