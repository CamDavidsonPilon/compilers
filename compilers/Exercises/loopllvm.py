# loopllvm.py
#
# An example of creating LLVM functions with a loop

# Example : LLVM code for the following function
#
#     func f(n int) int {
#          var total int = 0;
#          while n > 0 {
#               total = total + n;
#               n = n - 1;
#          }
#          return total;
#     }
#

from llvmlite.ir import (
    Module, IRBuilder, IntType, Function, FunctionType, Constant
    )

mod = Module('example')

# Declare the f function with our loop
f_func = Function(mod,
                  FunctionType(IntType(32), [IntType(32)]),
                  name='f')

block = f_func.append_basic_block("entry")
builder = IRBuilder(block)

# Copy the argument to a local variable.  For reasons, that are 
# complicated, we copy the function argument to a local variable
# allocated on the stack (this makes mutations of the variable
# easier when looping).

n_var = builder.alloca(IntType(32), name='n')
builder.store(f_func.args[0], n_var)

# Allocate the result variable
total_var = builder.alloca(IntType(32), name='total')
builder.store(Constant(IntType(32), 0), total_var)

# Make a new basic-block for the loop test
loop_test_block = f_func.append_basic_block('looptest')
builder.branch(loop_test_block)
builder.position_at_end(loop_test_block)

# Perform the comparison
testvar = builder.icmp_signed('>', builder.load(n_var), Constant(IntType(32), 0))

# Make three blocks
loop_body_block = f_func.append_basic_block('loopbody')
loop_exit_block = f_func.append_basic_block('loopexit')

# Branch based on the test var
builder.cbranch(testvar, loop_body_block, loop_exit_block)

builder.position_at_end(loop_body_block)
tmp = builder.add(builder.load(total_var), builder.load(n_var))
builder.store(tmp, total_var)
tmp2 = builder.sub(builder.load(n_var), Constant(IntType(32), 1))
builder.store(tmp2, n_var)
builder.branch(loop_test_block)

# Emit code in the loop-exit
builder.position_at_end(loop_exit_block)
builder.ret(builder.load(total_var))

print(mod)

print(':::: RUNNING ::::')

import llvmlite.binding as llvm

llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

target = llvm.Target.from_default_triple()
target_machine = target.create_target_machine()

compiled_mod = llvm.parse_assembly(str(mod))
engine = llvm.create_mcjit_compiler(compiled_mod, target_machine)

func_ptr = engine.get_function_address('f')

from ctypes import CFUNCTYPE, c_int
f = CFUNCTYPE(c_int, c_int)(func_ptr)

r = f(10)
print('Should get 55 -->', r)

r = f(100000)
print('Should get 705082704 -->', r)


