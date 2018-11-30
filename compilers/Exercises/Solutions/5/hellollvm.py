# hellollvm.py

from llvmlite.ir import (
    Module, Function, FunctionType, IntType,
    Constant, IRBuilder
    )

mod = Module('hello')
hello_func = Function(mod, 
                      FunctionType(IntType(32), []), 
                      name='hello')
block = hello_func.append_basic_block('entry')
builder = IRBuilder(block)
builder.ret(Constant(IntType(32), 37))

# A user-defined function
from llvmlite.ir import DoubleType

ty_double = DoubleType()
dsquared_func = Function(mod, 
                         FunctionType(ty_double, [ty_double, ty_double]), 
                         name='dsquared')
block = dsquared_func.append_basic_block('entry')
builder = IRBuilder(block)

# Get the function args
x, y = dsquared_func.args

# Compute temporary values for x*x and y*y
xsquared = builder.fmul(x, x)
ysquared = builder.fmul(y, y)

# Sum the values and return the result
d2 = builder.fadd(xsquared, ysquared)
builder.ret(d2)

# Part (e) - Calling an external function

sqrt_func = Function(mod, 
                     FunctionType(ty_double, [ty_double]), 
                     name='sqrt')

distance_func = Function(mod, 
                         FunctionType(ty_double, [ty_double, ty_double]), 
                         name='distance')

block = distance_func.append_basic_block('entry')
builder = IRBuilder(block)
x, y = distance_func.args
d2 = builder.call(dsquared_func, [x, y])
d = builder.call(sqrt_func, [d2])
builder.ret(d)

# Part (f) - Global variables

from llvmlite.ir import GlobalVariable, VoidType
x_var = GlobalVariable(mod, ty_double, 'x')
x_var.initializer = Constant(ty_double, 0.0)

incr_func = Function(mod, 
                     FunctionType(VoidType(), []), 
                     name='incr')

block = incr_func.append_basic_block("entry")
builder = IRBuilder(block)
tmp1 = builder.load(x_var)
tmp2 = builder.fadd(tmp1, Constant(ty_double, 1.0))
builder.store(tmp2, x_var)
builder.ret_void()

# Part (g) - JIT

import llvmlite.binding as llvm

llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

target = llvm.Target.from_default_triple()
target_machine = target.create_target_machine()
compiled_mod = llvm.parse_assembly(str(mod))
engine = llvm.create_mcjit_compiler(compiled_mod, target_machine)

# Look up the function pointer (a Python int)
func_ptr = engine.get_function_address("distance")

# Turn into a Python callable using ctypes
from ctypes import CFUNCTYPE, c_int, c_double
distance = CFUNCTYPE(c_double, c_double, c_double)(func_ptr)

res = distance(3, 4)
print('distance =', res)

