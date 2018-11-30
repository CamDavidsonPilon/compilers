# condllvm.py
#
# An example of creating LLVM functions with control flow

# Example 1 : LLVM code for the following function
#
#     func f(a int, b int) int {
#          var c int;
#          if a < b {
#               c = a + b;
#          } else {
#               c = a - b;
#          }
#          return c;
#     }
#

from llvmlite.ir import (
    Module, IRBuilder, IntType, Function, FunctionType
    )

mod = Module('example')
f_func = Function(mod,
                  FunctionType(IntType(32), [IntType(32), IntType(32)]),
                  name='f')

block = f_func.append_basic_block("entry")
builder = IRBuilder(block)

# Get the arguments
a_var, b_var = f_func.args

# Allocate the result variable
c_var = builder.alloca(IntType(32), name='c')

# Perform the comparison
testvar = builder.icmp_signed('<', a_var, b_var)

# Make three blocks
then_block = f_func.append_basic_block('then')
else_block = f_func.append_basic_block('else')
merge_block = f_func.append_basic_block('merge')

# Emit the branch instruction
builder.cbranch(testvar, then_block, else_block)

# Generate code in the then-branch
builder.position_at_end(then_block)
result = builder.add(a_var, b_var)
builder.store(result, c_var)
builder.branch(merge_block)

# Generate code in the else-branch
builder.position_at_end(else_block)
result = builder.sub(a_var, b_var)
builder.store(result, c_var)
builder.branch(merge_block)

# Emit code after the if-else
builder.position_at_end(merge_block)
builder.ret(builder.load(c_var))

print(mod)

print(":::: RUNNING ::::")


import llvmlite.binding as llvm

llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

target = llvm.Target.from_default_triple()
target_machine = target.create_target_machine()

compiled_mod = llvm.parse_assembly(str(mod))
engine = llvm.create_mcjit_compiler(compiled_mod, target_machine)

# Look up the function pointer (a Python int)
func_ptr = engine.get_function_address('f')

from ctypes import CFUNCTYPE, c_int
f = CFUNCTYPE(c_int, c_int, c_int)(func_ptr)

r = f(2, 3)
print('Should get 5 -->', r)

r = f(3, 2)
print('Should get 1 -->', r)

