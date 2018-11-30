# gone/interp.py
'''
Interpreter
===========

This is an interpreter than can run gone programs directly from the
generated IR code.  This can be used to check results without 
requiring an LLVM dependency.

To run a program use::

    bash % python3 -m gone.interp someprogram.g

'''
import sys

class Frame(object):
    '''
    Object representing a stack frame.
    '''
    def __init__(self, args):
        self.args = args
        self.vars = { 'return' : None }

    def __getitem__(self, name):
        return self.vars[name]

    def __setitem__(self, name, value):
        self.vars[name] = value

    def __contains__(self, name):
        return name in self.vars
        
class Interpreter(object):
    '''
    Runs an interpreter on the SSA intermediate code generated for
    your compiler.   The implementation idea is as follows.  Given
    a sequence of instruction tuples such as:

         code = [ 
              ('MOVI', 1, 'R1'),
              ('MOVI', 2, 'R2'),
              ('ADDI', 'R1', 'R2', 'R3'),
              ('PRINTI', 'R3')
              ...
         ]

    The class executes methods self.run_opcode(args).  For example:

             self.run_MOVI(1, 'R1')
             self.run_MOVI(2, 'R2')
             self.run_ADDI('R1','R2','R3')
             self.run_PRINTI('R3')
    '''
    def __init__(self):
        # Frame stack
        self.framestack = []

        # Current stack frame
        self.frame = None

        # Current program counter
        self.pc = 0

        # Global variables
        self.globals = {}

    # Add user-defined functions to the globals.  Builds a dictionary mapping function names
    # to the code associated with each function
    def register_functions(self, functionlist):
        self.functions = {}
        for func in functionlist:
            self.functions[func.name] = func

    def execute_function(self, funcname, args):
        '''
        Run intermediate code in the interpreter.  ircode is a list
        of instruction tuples.  Each instruction (opcode, *args) is 
        dispatched to a method self.run_opcode(*args)
        '''
        code = self.functions[funcname].code
        self.framestack.append((self.pc, self.frame))
        self.frame = Frame(args)

        # Bind arguments
        for name, arg in zip(self.functions[funcname].arg_names, args):
            self.frame[name] = arg
            
        self.pc = 0
        while self.pc < len(code):
            instr = code[self.pc]
            opcode = instr[0]
            self.pc += 1
            if hasattr(self, 'run_'+opcode):
                getattr(self, 'run_'+opcode)(*instr[1:])
            else:
                print('Warning: No run_'+opcode+'() method')
            if self.pc < 0:
                break
        result = self.frame['return']
        self.pc, self.frame = self.framestack.pop()
        return result

    def execute(self, code):
        for inst, *args in code:
            getattr(self, f'run_{inst}')(*args)
        
    # Interpreter opcodes
    def run_MOVI(self, value, target):
        self.frame[target] = value
    run_MOVF = run_MOVI
    run_MOVB = run_MOVI

    def run_ADDI(self, left, right, target):
        self.frame[target] = self.frame[left] + self.frame[right]
    run_ADDF = run_ADDI

    def run_SUBI(self, left, right, target):
        self.frame[target] = self.frame[left] - self.frame[right]
    run_SUBF = run_SUBI

    def run_MULI(self, left, right, target):
        self.frame[target] = self.frame[left] * self.frame[right]
    run_MULF = run_MULI

    def run_DIVI(self, left, right, target):
        self.frame[target] = self.frame[left] // self.frame[right]

    def run_DIVF(self, left, right, target):
        self.frame[target] = self.frame[left] / self.frame[right]

    def run_PRINTI(self, value):
        print(self.frame[value])
    run_PRINTF = run_PRINTI

    def run_PRINTB(self, value):
        print(chr(self.frame[value]), end='')
        sys.stdout.flush()

    def run_VARI(self, name):
        self.globals[name] = 0

    def run_VARF(self, name):
        self.globals[name] = 0.0

    def run_VARB(self, name):
        self.globals[name] = 0

    def run_ALLOCI(self, name):
        self.frame[name] = 0

    def run_ALLOCF(self, name):
        self.frame[name] = 0.0

    def run_ALLOCB(self, name):
        self.frame[name] = 0

    def run_LOADI(self, name, target):
        if name in self.frame:
            self.frame[target] = self.frame[name]
        else:
            self.frame[target] = self.globals[name]
    run_LOADF = run_LOADI
    run_LOADB = run_LOADI

    def run_STOREI(self, target, name):
        if name in self.frame:
            self.frame[name] = self.frame[target]
        else:
            self.globals[name] = self.frame[target]

    run_STOREF = run_STOREI
    run_STOREB = run_STOREI

    def run_LABEL(self, label):
        pass

    def run_CALL(self, funcname, *args):
        '''
        Call a previously declared external function.
        '''
        target = args[-1]
        argvals = [self.frame[name] for name in args[:-1]]
        if funcname in self.functions:
            result = self.execute_function(funcname, argvals)
            self.frame[target] = result
        else:
            raise RuntimeError('No function %s found' % name)

    def run_BRANCH(self, target):
        self.pc = target

    def run_CBRANCH(self, testvar, true_target, false_target):
        if self.frame[testvar]:
            self.pc = true_target
        else:
            self.pc = false_target

    def run_RET(self, retvar):
        self.frame['return'] = self.frame[retvar]
        self.pc = -1

    def run_CMPI(self, op, r1, r2, target):
        if op == '<':
            self.frame[target] = self.frame[r1] < self.frame[r2]
        elif op == '<=':
            self.frame[target] = self.frame[r1] <= self.frame[r2]
        elif op == '>':
            self.frame[target] = self.frame[r1] > self.frame[r2]
        elif op == '>=':
            self.frame[target] = self.frame[r1] >= self.frame[r2]
        elif op == '==':
            self.frame[target] = self.frame[r1] == self.frame[r2]
        elif op == '!=':
            self.frame[target] = self.frame[r1] != self.frame[r2]

    run_CMPF = run_CMPI
    run_CMPB = run_CMPI

# Linker.  This walks the instruction sequence and replaces block
# references with instruction addresses in branch instructions.

def link(ircode):
    # Make the block map
    blocks = { op[1]: n for n, op in enumerate(ircode)
               if op[0] == 'LABEL' }

    newcode = []
    for instr in ircode:
        if instr[0] == 'BRANCH':
            newcode.append(('BRANCH', blocks[instr[1]]))
        elif instr[0] == 'CBRANCH':
            newcode.append(('CBRANCH', instr[1], blocks[instr[2]], blocks[instr[3]]))
        else:
            newcode.append(instr)

    return newcode

# ----------------------------------------------------------------------
#                       DO NOT MODIFY ANYTHING BELOW       
# ----------------------------------------------------------------------

def main():
    import sys
    from .ircode import compile_ircode
    from .errors import errors_reported

    if len(sys.argv) != 2:
        sys.stderr.write('Usage: python3 -m gone.interp filename\n')
        raise SystemExit(1)

    source = open(sys.argv[1]).read()
    functions = compile_ircode(source)
    if not errors_reported():
        # Take the list of functions and build fully linked versions
        linked_functions = []
        for func in functions:
            func.code = link(func.code)
            linked_functions.append(func)

        interpreter = Interpreter()
        interpreter.register_functions(linked_functions)
        # Execute the __init function which is responsible for global vars and constants
        interpreter.execute_function('__init', [])

        # Execute the main() entry point
        result = interpreter.execute_function('main',[])
        print('Program Returned: %d' % result)

if __name__ == '__main__':
    main()






        
        
        
