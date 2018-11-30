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

CPUs also feature a small set of core datatypes such as integers,
bytes, and floats. There are dedicated instructions for each type.
For example:

    ADDI   R1, R2, R3        ; Integer add
    ADDF   R4, R5, R6        ; Float add

There is often a disconnect between the types used in the source
programming language and the generated IRCode.  For example, a target
machine might only have integers and floats.  To represent a value
such as a boolean, you have to represent it as one of the native types
such as an integer.   This is an implementation detail that users
won't worry about (they'll never see it, but you'll have to worry
about it in the compiler).

Here is an instruction set specification for our IRCode:

    MOVI   value, target       ;  Load a literal integer
    VARI   name                ;  Declare an integer variable
    ALLOCI name                ;  Allocate an integer variabe on the stack
    LOADI  name, target        ;  Load an integer from a variable
    STOREI target, name        ;  Store an integer into a variable
    ADDI   r1, r2, target      ;  target = r1 + r2
    SUBI   r1, r2, target      ;  target = r1 - r2
    MULI   r1, r2, target      ;  target = r1 * r2
    DIVI   r1, r2, target      ;  target = r1 / r2
    PRINTI source              ;  print source  (debugging)
    CMPI   op, r1, r2, target  ;  Compare r1 op r2 -> target
    AND    r1, r2, target      :  target = r1 & r2
    OR     r1, r2, target      :  target = r1 | r2
    XOR    r1, r2, target      :  target = r1 ^ r2
    ITOF   r1, target          ;  target = float(r1)

    BLK   name                 ; Declare a block
    JMP   target_block         ; JMP to target block
    CJMP   source, true_block , false_block

    MOVF   value, target       ;  Load a literal float
    VARF   name                ;  Declare a float variable
    ALLOCF name                ;  Allocate a float variable on the stack
    LOADF  name, target        ;  Load a float from a variable
    STOREF target, name        ;  Store a float into a variable
    ADDF   r1, r2, target      ;  target = r1 + r2
    SUBF   r1, r2, target      ;  target = r1 - r2
    MULF   r1, r2, target      ;  target = r1 * r2
    DIVF   r1, r2, target      ;  target = r1 / r2
    PRINTF source              ;  print source (debugging)
    CMPF   op, r1, r2, target  ;  r1 op r2 -> target
    FTOI   r1, target          ;  target = int(r1)

    MOVB   value, target       ; Load a literal byte
    VARB   name                ; Declare a byte variable
    ALLOCB name                ; Allocate a byte variable
    LOADB  name, target        ; Load a byte from a variable
    STOREB target, name        ; Store a byte into a variable
    PRINTB source              ; print source (debugging)
    BTOI   r1, target          ; Convert a byte to an integer
    ITOB   r2, target          ; Truncate an integer to a byte
    CMPB   op, r1, r2, target  ; r1 op r2 -> target

There are also some control flow instructions

    LABEL  name                  ; Declare a label
    BRANCH label                 ; Unconditionally branch to label
    CBRANCH test, label1, label2 ; Conditional branch to label1 or label2 depending on test being 0 or not
    CALL   name, arg0, arg1, ... argN, target    ; Call a function name(arg0, ... argn) -> target
    RET    r1                    ; Return a result from a function

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
from . import typesys

class GenerateCode(ast.NodeVisitor):
    '''
    Node visitor class that creates 3-address encoded instruction sequences.
    '''
    def __init__(self):
        # counter for registers
        self.register_count = 0
        self.block_count = 0
        # The generated code (list of tuples)
        self.code = []

    def new_register(self):
         '''
         Creates a new temporary register
         '''
         self.register_count += 1
         return f'R{self.register_count}'

    def new_block(self):
         '''
         Creates a new temporary register
         '''
         self.block_count += 1
         return f'B{self.block_count}'

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

    def visit_BoolLiteral(self, node):
        target = self.new_register()
        self.code.append(('MOVI', 1 if node.value == 'true' else 0, target))
        node.register = target

    def visit_IfConditional(self, node):
        # create three blocks (true, false, finally)

        # where are we going?
        self.visit(node.switch)
        true_block_name = self.new_block()
        false_block_name = self.new_block()
        finally_block_name = self.new_block()

        # create the cjump instruction
        inst = ('CJMP', node.switch.register, true_block_name, false_block_name)
        self.code.append(inst)

        inst = ('BLK', true_block_name)
        self.code.append(inst)

        # do the True code path
        self.visit(node.true_path)

        # append jump to finally
        inst = ('JMP', finally_block_name)
        self.code.append(inst)


        # append False block
        inst = ('BLK', false_block_name)
        self.code.append(inst)

        # do the False code path
        self.visit(node.false_path)

        # append jump to finally
        inst = ('JMP', finally_block_name)
        self.code.append(inst)

        # append the Finally block
        inst = ('BLK', finally_block_name)
        self.code.append(inst)

    def visit_WhileConditional(self, node):

        true_block_name = self.new_block()
        finally_block_name = self.new_block()

        # create the cjump instruction
        self.visit(node.switch)
        self.code.append(('CJMP', node.switch.register, true_block_name, finally_block_name))
        self.code.append(('BLK', true_block_name))

        # execute the internal statements
        self.visit(node.statements)

        # visit the switch again to load into proper register
        self.visit(node.switch)
        self.code.append(('CJMP', node.switch.register, true_block_name, finally_block_name))
        self.code.append(('BLK', finally_block_name))


    def visit_UnaryOp(self, node):
        self.visit(node.right)
        op = node.op
        target = self.new_register()
        if op == '+':
            # we skip this instruction.
            node.register = node.right.register
            return
        elif (op == '-') or (op == '!'):
            if (node.type == typesys.INT):
                code = 'SUBI'
                zero_node = ast.IntegerLiteral(0)
                self.visit_IntegerLiteral(zero_node)
            if (node.type == typesys.BOOL):
                code = 'SUBI'
                zero_node = ast.IntegerLiteral(1)
                self.visit_IntegerLiteral(zero_node)
            elif node.type == typesys.FLOAT:
                code = 'SUBF'
                zero_node = ast.FloatLiteral(0.0)
                self.visit_FloatLiteral(zero_node)

            inst = (code, zero_node.register, node.right.register, target)
            node.register = target
            self.code.append(inst)
        else:
            raise RuntimeError(f'Unknown unary {op}')

    def visit_FunctionDeclaration(self, node):
        inst = ('FUNCTION',
                node.name,
                "(" + ','.join(map(lambda a: str((a.type, a.name)), node.arguments)) + ")",
                node.return_type.type)
        self.code.append(inst)
        self.visit(node.statements)
        # append return statement
        inst = ('RETURN', node.return_name)
        self.code.append(inst)

        inst = ('FUNCTION_END', node.name)
        self.code.append(inst)


    def visit_Parameter(self, node):
        self.visit(node.value)
        node.register = node.value.register

    def visit_FunctionCall(self, node):
        self.visit(node.params)

        target = self.new_register()
        inst = ('CALL', node.name.name, '(' + ','.join(map(lambda a: "'" + a.register + "'", node.params)) + ')', target)
        self.code.append(inst)
        node.register = target

    def visit_Statements(self, node):
        # am I in a function or not?
        self.visit(node.statements)


    def visit_BinOp(self, node):
        """
        ADDI   r1, r2, target      ;  target = r1 + r2
        SUBI   r1, r2, target      ;  target = r1 - r2
        MULI   r1, r2, target      ;  target = r1 * r2
        DIVI   r1, r2, target      ;  target = r1 / r2
        CMPI   op, r1, r2, target  ;  Compare r1 op r2 -> target
        AND    r1, r2, target      :  target = r1 & r2
        OR     r1, r2, target      :  target = r1 | r2

        """
        self.visit(node.left)
        self.visit(node.right)
        op = node.op
        target = self.new_register()
        cmp_type = node.left.type # the same as right, as we type checked

        suffix = {typesys.INT: 'I', typesys.FLOAT: 'F', typesys.BOOL: 'I'}[cmp_type]

        if op in {'<', '>', '!=', '==', '<=', '>='}:
            code = 'CMP'
            code += suffix
            inst = (code, op, node.left.register, node.right.register, target)
        elif op in {'&&', '||'}:
            code = {'&&': 'AND', '||': 'OR'}[op]
            inst = (code, node.left.register, node.right.register, target)
        else:
            code = {'+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV'}[op]
            code += suffix
            inst = (code, node.left.register, node.right.register, target)

        self.code.append(inst)
        node.register = target


    def visit_ConstDeclaration(self, node):
        # this will always assign
        #     VARI   name
        value = node.value
        self.visit(value)

        if hasattr(value, 'local_context'):
            if node.type == typesys.INT:
                code_v, code_s = 'ALLOCI', 'STOREI'
            elif node.type == typesys.FLOAT:
                code_v, code_s = 'ALLOCF', 'STOREF'
            elif node.type == typesys.CHAR:
                code_v, code_s = 'ALLOCB', 'STOREB'
            elif node.type == typesys.BOOL:
                code_v, code_s = 'ALLOCI', 'STOREI'

        else:
            if node.type == typesys.INT:
                code_v, code_s = 'VARI', 'STOREI'
            elif node.type == typesys.FLOAT:
                code_v, code_s = 'VARF', 'STOREF'
            elif node.type == typesys.CHAR:
                code_v, code_s = 'VARB', 'STOREB'
            elif node.type == typesys.BOOL:
                code_v, code_s = 'VARI', 'STOREI'

        # declare variable
        inst = (code_v, node.name)
        self.code.append(inst)

        # store variable
        inst = (code_s, value.register, node.name)
        self.code.append(inst)


    def visit_VarDeclaration(self, node):
        # this may not always assign
        #     VARI   name

        value = node.value
        self.visit(value)

        if hasattr(value, 'local_context'):
            if node.type == typesys.INT:
                code_v, code_s = 'ALLOCI', 'STOREI'
            elif node.type == typesys.FLOAT:
                code_v, code_s = 'ALLOCF', 'STOREF'
            elif node.type == typesys.CHAR:
                code_v, code_s = 'ALLOCB', 'STOREB'
            elif node.type == typesys.BOOL:
                code_v, code_s = 'ALLOCI', 'STOREI'

        else:
            if node.type == typesys.INT:
                code_v, code_s = 'VARI', 'STOREI'
            elif node.type == typesys.FLOAT:
                code_v, code_s = 'VARF', 'STOREF'
            elif node.type == typesys.CHAR:
                code_v, code_s = 'VARB', 'STOREB'
            elif node.type == typesys.BOOL:
                code_v, code_s = 'VARI', 'STOREI'

        inst = (code_v, node.name)
        self.code.append(inst)

        if value is not None:
            inst = (code_s, node.value.register, node.name)
            self.code.append(inst)

    def visit_Assignment(self, node):
        #import pdb
        #pdb.set_trace()
        self.visit(node.value)

        if node.type == typesys.INT:
            code = 'STOREI'
        elif node.type == typesys.FLOAT:
            code = 'STOREF'
        elif node.type == typesys.CHAR:
            code = 'STOREB'
        elif node.type == typesys.BOOL:
            code = 'STOREI'

        inst = (code, node.value.register, node.location.name)
        self.code.append(inst)

    def visit_SimpleLocation(self, node):

        target = self.new_register()
        if node.type == typesys.INT:
            code = 'LOADI'
        elif node.type == typesys.FLOAT:
            code = 'LOADF'
        elif node.type == typesys.CHAR:
            code = 'LOADB'
        elif node.type == typesys.BOOL:
            code = 'LOADI'

        inst = (code, node.name, target)
        self.code.append(inst)
        node.register = target


    def visit_PrintStatement(self, node):
        self.visit(node.value)
        if node.value.type == typesys.INT:
            code = 'PRINTI'
        elif node.value.type == typesys.FLOAT:
            code = 'PRINTF'
        elif node.value.type == typesys.CHAR:
            code = 'PRINTB'
        elif node.value.type == typesys.BOOL:
            code = 'PRINTI'

        inst = (code, node.value.register)
        self.code.append(inst)

# ----------------------------------------------------------------------
#                          TESTING/MAIN PROGRAM
#
# Note: Some changes will be required in later projects.
# ----------------------------------------------------------------------

def compile_ircode(source):
    '''
    Generate intermediate code from source.
    '''
    from .parser import parse, flatten
    from .checker import check_program
    from .errors import errors_reported

    ast = parse(source)

    check_program(ast)

    for depth, node in flatten(ast):
        print('%s: %s%s type: %s' % (getattr(node, 'lineno', None), ' '*(4*depth), node,
                                     getattr(node, 'type', None)))

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
