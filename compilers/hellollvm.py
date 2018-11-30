# hellollvm.py

from llvmlite.ir import (
    Module, Function, FunctionType, IntType,
    Constant, IRBuilder
    )
from llvmlite.ir import DoubleType

mod = Module('hello')

hello_func = Function(mod, FunctionType(IntType(32), []), name='hello')
block = hello_func.append_basic_block('entry')
builder = IRBuilder(block)
builder.ret(Constant(IntType(32), 37))

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


from llvmlite.ir import VoidType

from llvmlite.ir import GlobalVariable
x_var = GlobalVariable(mod, ty_double, 'x')
x_var.initializer = Constant(ty_double, 0.0)

incr_func = Function(mod,
                     FunctionType(VoidType(), []),
                     name='incr')
block = incr_func.append_basic_block('entry')
builder = IRBuilder(block)
tmp1 = builder.load(x_var)
tmp2 = builder.fadd(tmp1, Constant(ty_double, 1.0))
builder.store(tmp2, x_var)
builder.ret_void()

# Output the final module
print(mod)

