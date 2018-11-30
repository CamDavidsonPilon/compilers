# cmp.py
# 
# A sample of executing an integer < in LLVM

from llvmlite.ir import (
    Module, Function, FunctionType, IntType, IRBuilder
)

mod = Module('example')

# Define a function:
#
#    func lessthan(x int, y int) bool {
#         return x < y;
#    }
# 
# Note: The result of boolean operations is a 1-bit integer

func = Function(mod, 
                FunctionType(IntType(1), [IntType(32), IntType(32)]),
                name = 'lessthan')

block = func.append_basic_block("entry")
builder = IRBuilder(block)

# The icmp_signed() instruction is used for all comparisons on
# integers.  For floating point, use fcmp_ordered().  The compare operation
# takes an operator expressed as a string such as '<', '>', '==',
# etc.

result =  builder.icmp_signed('<', func.args[0], func.args[1])
builder.ret(result)

# ---- Test Code

import llvmlite.binding as llvm

llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

target = llvm.Target.from_default_triple()
target_machine = target.create_target_machine()

compiled_mod = llvm.parse_assembly(str(mod))
engine = llvm.create_mcjit_compiler(compiled_mod, target_machine)

func_ptr = engine.get_function_address('lessthan')
from ctypes import CFUNCTYPE, c_int
lessthan = CFUNCTYPE(c_int, c_int, c_int)(func_ptr)

x = 3
y = 4

# Evaluate x < y
r = lessthan(x, y)
print('Should get 1 -->', r)

# Evaluate y < x
r = lessthan(y, x)
print('Should get 0 -->', r)




